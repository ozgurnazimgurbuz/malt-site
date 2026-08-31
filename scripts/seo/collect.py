#!/usr/bin/env python3
"""GEO/SEO BEFORE collector. Reads built HTML; writes artifacts. Does not mutate the site."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[2]
BENCH = ROOT / "seo" / "benchmark"
OUT = ROOT / "artifacts" / "geo-seo" / "before"
SITE = "https://maltstudio.co"
HOME = SITE + "/"

GEO_SCORE_URLS = [
    HOME,
    f"{SITE}/hizmetler/tabela/",
    f"{SITE}/bilgi/tabela-cesitleri/",
    f"{SITE}/bolgeler/tekirdag/",
    f"{SITE}/projeler/ofiso/",
]

EEAT_FINGERPRINT = "Üretim, deneyim ve yerel uzmanlık"
LEGAL_PATHS = ("/kvkk/", "/gizlilik/", "/privacy/", "/cerez-politikasi/")
BOT_AGENTS = ("GPTBot", "ClaudeBot", "Google-Extended")
BUSINESS_ID = f"{SITE}/#business"
WEBSITE_ID = f"{SITE}/#website"

SKIP_TAGS = frozenset({"script", "style", "noscript", "template"})
BLOCK_TAGS = frozenset({"p", "li", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "figcaption", "dt", "dd"})

LD_RE = re.compile(
    r"<script([^>]*type=['\"]application/ld\+json['\"][^>]*)>(.*?)</script>",
    re.I | re.S,
)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
CANON_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*>', re.I)
HREF_IN_TAG = re.compile(r'\bhref=["\']([^"\']+)["\']', re.I)
CONTENT_IN_TAG = re.compile(r'\bcontent=["\']([^"\']*)["\']', re.I)
META_RE = re.compile(r"<meta\b([^>]*)/?>", re.I)
LINK_RE = re.compile(r"<link\b([^>]*)/?>", re.I)
ATTR = re.compile(r"""([a-zA-Z_:][\w:.-]*)\s*=\s*(['"])(.*?)\2""", re.S)
BR_H2_RE = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.I | re.S)
DETAILS_RE = re.compile(r"<details\b[^>]*>(.*?)</details>", re.I | re.S)
SUMMARY_RE = re.compile(r"<summary\b[^>]*>(.*?)</summary>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_urls() -> list[str]:
    urls = []
    for line in (BENCH / "urls.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        urls.append(line)
    return urls


def sha256_text(*parts: str) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def attrs(blob: str) -> dict[str, str]:
    return {m.group(1).lower(): m.group(3) for m in ATTR.finditer(blob)}


def strip_tags(html: str, br: str = " ") -> str:
    html = re.sub(r"<br\s*/?>", br, html, flags=re.I)
    html = TAG_RE.sub(" ", html)
    return WS_RE.sub(" ", html).strip()


def words(text: str) -> list[str]:
    return [w for w in re.split(r"\s+", text) if w]


def url_path(url: str) -> str:
    p = urlparse(url).path
    return p if p else "/"


def url_to_html(url: str) -> Path:
    path = url_path(url)
    if path in ("", "/"):
        return ROOT / "index.html"
    rel = path.lstrip("/")
    if path.endswith("/"):
        return ROOT / rel / "index.html"
    candidate = ROOT / rel
    if candidate.is_file():
        return candidate
    return ROOT / rel / "index.html"


def url_to_md(url: str) -> Path:
    html = url_to_html(url)
    return Path(str(html) + ".md")


def url_slug(url: str) -> str:
    path = url_path(url)
    if path in ("", "/"):
        return "home"
    return path.strip("/").replace("/", "--")


def is_internal(href: str) -> bool:
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return False
    if href.startswith("#") or href.startswith("/"):
        return True
    host = urlparse(href).netloc.lower()
    return host in ("", "maltstudio.co", "www.maltstudio.co")


def absolutize(href: str, page_url: str) -> str:
    if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return href
    if href.startswith("#"):
        return urljoin(page_url, href)
    return urljoin(page_url, href)


def normalize_page_url(url: str) -> str:
    p = urlparse(url)
    path = p.path or "/"
    if path != "/" and not path.endswith("/"):
        # directory pages in this site always use trailing slash
        if not Path(path).suffix:
            path = path + "/"
    if p.netloc in ("www.maltstudio.co", "maltstudio.co") or not p.netloc:
        return f"{SITE}{path}"
    return url


def git_state() -> dict[str, Any]:
    def run(args: list[str]) -> str:
        try:
            return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        except Exception:
            return ""

    return {
        "branch": run(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "sha": run(["git", "rev-parse", "HEAD"]),
        "status": run(["git", "status", "--porcelain"]),
        "status_full": run(["git", "status"]),
    }


def pkg_versions() -> dict[str, str]:
    out = {"python": sys.version.split()[0], "python_full": sys.version}
    try:
        from PIL import Image  # noqa: F401

        import PIL

        out["Pillow"] = getattr(PIL, "__version__", "unknown")
    except Exception:
        out["Pillow"] = "not-importable"
    out["lighthouse"] = "not-installed"
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    out["chrome_binary"] = chrome if Path(chrome).exists() else "not-found"
    return out


class PageHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.headings: list[dict[str, str]] = []
        self._h: str | None = None
        self._h_parts: list[str] = []
        self.imgs: list[dict[str, Any]] = []
        self.sources: list[dict[str, str]] = []
        self.picture_count = 0
        self.in_picture = 0
        self.anchors: list[dict[str, str]] = []
        self._a_href = ""
        self._a_rel = ""
        self._a_parts: list[str] = []
        self.tables = 0
        self.ols = 0
        self.uls = 0
        self.breadcrumb_html = False
        self.faqs: list[dict[str, str]] = []
        self._in_summary = False
        self._summary_parts: list[str] = []
        self._in_details = 0
        self._details_answer: list[str] = []
        self.paras: list[str] = []
        self._in_p = False
        self._p_parts: list[str] = []
        self.in_main = 0
        self.main_parts: list[str] = []
        self.body_parts: list[str] = []
        self.data_prerendered = False
        self.h1: list[str] = []
        self.in_header = 0
        self.in_footer = 0
        self.in_nav = 0

    def handle_starttag(self, tag: str, attrs_in) -> None:
        ad = {k.lower(): (v or "") for k, v in attrs_in}
        if tag in SKIP_TAGS:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "body" and "data-prerendered" in ad:
            self.data_prerendered = True
        if tag == "main":
            self.in_main += 1
        if tag == "header":
            self.in_header += 1
        if tag == "footer":
            self.in_footer += 1
        if tag == "nav":
            self.in_nav += 1
            label = (ad.get("aria-label") or ad.get("class") or "").lower()
            if "breadcrumb" in label or "breadcrumb" in ad.get("class", ""):
                self.breadcrumb_html = True
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._h = tag
            self._h_parts = []
        if tag == "picture":
            self.picture_count += 1
            self.in_picture += 1
        if tag == "source":
            self.sources.append(
                {
                    "type": ad.get("type", ""),
                    "srcset": ad.get("srcset", ""),
                    "in_picture": self.in_picture > 0,
                }
            )
        if tag == "img":
            self.imgs.append(
                {
                    "src": ad.get("src", ""),
                    "alt": ad.get("alt", ""),
                    "width": ad.get("width", ""),
                    "height": ad.get("height", ""),
                    "loading": ad.get("loading", ""),
                    "decoding": ad.get("decoding", ""),
                    "fetchpriority": ad.get("fetchpriority", ""),
                    "in_picture": self.in_picture > 0,
                    "class": ad.get("class", ""),
                }
            )
        if tag == "a":
            self._a_href = ad.get("href", "")
            self._a_rel = ad.get("rel", "")
            self._a_parts = []
        if tag == "table":
            self.tables += 1
        if tag == "ol":
            self.ols += 1
        if tag == "ul":
            self.uls += 1
        if tag == "details":
            self._in_details += 1
            self._details_answer = []
        if tag == "summary" and self._in_details:
            self._in_summary = True
            self._summary_parts = []
        if tag == "p":
            self._in_p = True
            self._p_parts = []
        if tag == "br" and self._h:
            self._h_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS:
            if self.skip:
                self.skip -= 1
            return
        if self.skip:
            return
        if tag == "main" and self.in_main:
            self.in_main -= 1
        if tag == "header" and self.in_header:
            self.in_header -= 1
        if tag == "footer" and self.in_footer:
            self.in_footer -= 1
        if tag == "nav" and self.in_nav:
            self.in_nav -= 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._h == tag:
            raw = "".join(self._h_parts)
            text_space = WS_RE.sub(" ", raw.replace("\n", " ")).strip()
            text_concat = WS_RE.sub(" ", raw.replace("\n", "")).strip()
            item = {"tag": tag, "text": text_space, "text_br_stripped": text_concat}
            self.headings.append(item)
            if tag == "h1":
                self.h1.append(text_space)
            self._h = None
        if tag == "picture" and self.in_picture:
            self.in_picture -= 1
        if tag == "a":
            self.anchors.append(
                {
                    "href": self._a_href,
                    "rel": self._a_rel,
                    "text": WS_RE.sub(" ", "".join(self._a_parts)).strip(),
                }
            )
            self._a_href = ""
        if tag == "summary":
            self._in_summary = False
        if tag == "details" and self._in_details:
            q = WS_RE.sub(" ", "".join(self._summary_parts)).strip()
            a = WS_RE.sub(" ", "".join(self._details_answer)).strip()
            self.faqs.append({"q": q, "a": a, "a_words": len(words(a))})
            self._in_details -= 1
        if tag == "p" and self._in_p:
            t = WS_RE.sub(" ", "".join(self._p_parts)).strip()
            if t:
                self.paras.append(t)
            self._in_p = False

    def handle_data(self, data: str) -> None:
        if self.skip or not data:
            return
        if self._h:
            self._h_parts.append(data)
        if self._a_href:
            self._a_parts.append(data)
        if self._in_summary:
            self._summary_parts.append(data)
        elif self._in_details:
            self._details_answer.append(data)
        if self._in_p:
            self._p_parts.append(data)
        if self.in_header or self.in_footer or self.in_nav:
            return
        if self.in_main:
            self.main_parts.append(data)
        self.body_parts.append(data)


def parse_ld_blocks(html: str) -> list[dict[str, Any]]:
    blocks = []
    for i, m in enumerate(LD_RE.finditer(html)):
        raw = m.group(2).strip()
        rec: dict[str, Any] = {
            "index": i,
            "raw": raw,
            "parse_ok": False,
            "error": None,
            "data": None,
        }
        if not raw:
            rec["error"] = "empty"
            blocks.append(rec)
            continue
        try:
            rec["data"] = json.loads(raw)
            rec["parse_ok"] = True
        except json.JSONDecodeError as e:
            rec["error"] = str(e)
        blocks.append(rec)
    return blocks


def walk_nodes(data: Any) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []

    def add(obj: Any) -> None:
        if isinstance(obj, list):
            for x in obj:
                add(x)
            return
        if not isinstance(obj, dict):
            return
        if "@graph" in obj:
            add(obj.get("@graph"))
            rest = {k: v for k, v in obj.items() if k != "@graph"}
            if rest.get("@type") or rest.get("@id"):
                nodes.append(obj)
            return
        nodes.append(obj)

    add(data)
    return nodes


def type_list(node: dict[str, Any]) -> list[str]:
    t = node.get("@type")
    if isinstance(t, list):
        return [str(x) for x in t]
    if t:
        return [str(t)]
    return []


def flatten_ids(obj: Any) -> list[str]:
    found = []
    if isinstance(obj, dict):
        if "@id" in obj and len(obj) == 1:
            found.append(str(obj["@id"]))
        elif "@id" in obj:
            found.append(str(obj["@id"]))
        for v in obj.values():
            found.extend(flatten_ids(v))
    elif isinstance(obj, list):
        for x in obj:
            found.extend(flatten_ids(x))
    return found


def ld_summary(blocks: list[dict[str, Any]], page_url: str) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    parse_failures = []
    for b in blocks:
        if not b["parse_ok"]:
            parse_failures.append({"index": b["index"], "error": b["error"]})
            continue
        nodes.extend(walk_nodes(b["data"]))

    defined_ids = []
    types: list[str] = []
    important: list[dict[str, Any]] = []
    for n in nodes:
        tid = n.get("@id")
        if tid:
            defined_ids.append(str(tid))
        types.extend(type_list(n))
        props = {
            k: n.get(k)
            for k in (
                "@id",
                "@type",
                "name",
                "url",
                "telephone",
                "email",
                "address",
                "geo",
                "openingHoursSpecification",
                "openingHours",
                "sameAs",
                "logo",
                "image",
                "description",
                "knowsAbout",
                "hasMap",
                "isPartOf",
                "about",
                "provider",
                "publisher",
                "mainEntity",
                "dateModified",
                "headline",
            )
            if k in n
        }
        if props:
            important.append(props)

    ref_ids = []
    for n in nodes:
        for key in ("isPartOf", "about", "provider", "publisher", "mainEntity"):
            v = n.get(key)
            if isinstance(v, dict) and "@id" in v:
                ref_ids.append(str(v["@id"]))
            elif isinstance(v, str) and v.startswith("http"):
                ref_ids.append(v)

    defined_set = set(defined_ids)
    dangling = sorted({r for r in ref_ids if r not in defined_set})

    id_types: dict[str, list[str]] = defaultdict(list)
    for n in nodes:
        if n.get("@id"):
            id_types[str(n["@id"])].extend(type_list(n))
    conflicts = []
    for iid, ts in id_types.items():
        uniq = sorted(set(ts))
        if len(uniq) > 1:
            conflicts.append({"id": iid, "types": uniq})

    dup_ids = [i for i, c in Counter(defined_ids).items() if c > 1]

    has_geo = False
    has_hours = False
    has_logo = False
    knows = []
    same_as = []
    for n in nodes:
        if n.get("geo"):
            has_geo = True
        if n.get("openingHoursSpecification") or n.get("openingHours"):
            has_hours = True
        if n.get("logo") or (n.get("image") and "LocalBusiness" in type_list(n)):
            has_logo = True
        if n.get("knowsAbout"):
            k = n["knowsAbout"]
            knows = k if isinstance(k, list) else [k]
        if n.get("sameAs"):
            s = n["sameAs"]
            same_as = s if isinstance(s, list) else [s]

    is_home = page_url.rstrip("/") == SITE or page_url == HOME
    return {
        "block_count": len(blocks),
        "parse_ok": all(b["parse_ok"] for b in blocks) if blocks else True,
        "parse_failures": parse_failures,
        "schema_types": sorted(set(types)),
        "defined_ids": defined_ids,
        "dangling_refs": dangling,
        "duplicate_ids": dup_ids,
        "conflicting_ids": conflicts,
        "important_properties": important,
        "has_geo": has_geo,
        "has_hours": has_hours,
        "has_logo_or_image": has_logo,
        "knowsAbout": knows,
        "sameAs": same_as,
        "homepage_schema": is_home,
        "has_website_node": WEBSITE_ID in defined_set,
        "has_business_node": BUSINESS_ID in defined_set,
        "has_faqpage": "FAQPage" in types,
        "has_article": any(t in types for t in ("Article", "TechArticle")),
        "has_service": "Service" in types,
        "has_breadcrumb_list": "BreadcrumbList" in types,
        "has_localbusiness": "LocalBusiness" in types,
        "has_webpage": "WebPage" in types,
        "ispartof_website": any(
            isinstance(n.get("isPartOf"), dict) and n["isPartOf"].get("@id") == WEBSITE_ID for n in nodes
        ),
    }


def heading_skips(headings: list[dict[str, str]]) -> list[str]:
    issues = []
    last = 0
    for h in headings:
        level = int(h["tag"][1])
        if last and level > last + 1:
            issues.append(f"h{last} -> h{level} ({h['text'][:80]})")
        last = level
    return issues


def parse_redirects() -> list[dict[str, str]]:
    rules = []
    text = (ROOT / "_redirects").read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        rules.append({"from": parts[0], "to": parts[1], "status": parts[2]})
    return rules


def match_redirect(path: str, rules: list[dict[str, str]]) -> dict[str, str] | None:
    variants = [path]
    if path.endswith("/") and path != "/":
        variants.append(path[:-1])
    else:
        variants.append(path + "/")
    for r in rules:
        src = r["from"]
        if src.endswith("/*"):
            prefix = src[:-1]  # keep slash
            for v in variants:
                if v.startswith(prefix[:-1]) or v.startswith(src[:-2]):
                    return r
        if src in variants:
            return r
    return None


def local_exists(url: str) -> bool:
    p = url_to_html(url)
    return p.is_file()


def parse_page(url: str) -> dict[str, Any]:
    path = url_to_html(url)
    rec: dict[str, Any] = {
        "url": url,
        "local_path": str(path.relative_to(ROOT)) if path.exists() or True else "",
        "status": 200 if path.is_file() else 0,
        "title": "",
        "description": "",
        "canonical": "",
        "robots": "",
        "h1": [],
        "headings": [],
        "internal_links": [],
        "word_count": 0,
        "indexable": False,
        "structured_data": [],
        "schema_types": [],
        "image_count": 0,
        "image_sources": [],
        "html_bytes": 0,
    }
    if not path.is_file():
        rec["error"] = "local HTML missing"
        return rec
    raw = path.read_bytes()
    rec["html_bytes"] = len(raw)
    html = raw.decode("utf-8")

    tm = TITLE_RE.search(html)
    rec["title"] = strip_tags(tm.group(1)) if tm else ""

    metas = {}
    for m in META_RE.finditer(html):
        a = attrs(m.group(1))
        key = a.get("name") or a.get("property") or a.get("http-equiv") or ""
        if key:
            metas[key.lower()] = a.get("content", "")
    rec["description"] = metas.get("description", "")
    rec["robots"] = metas.get("robots", "")
    rec["og_title"] = metas.get("og:title", "")
    rec["og_description"] = metas.get("og:description", "")
    rec["og_image"] = metas.get("og:image", "")
    rec["og_image_alt"] = metas.get("og:image:alt", "")
    rec["og_url"] = metas.get("og:url", "")
    rec["twitter_title"] = metas.get("twitter:title", "")
    rec["twitter_description"] = metas.get("twitter:description", "")
    rec["twitter_image"] = metas.get("twitter:image", "")
    rec["twitter_image_alt"] = metas.get("twitter:image:alt", "")
    rec["twitter_card"] = metas.get("twitter:card", "")
    rec["gsc_verification"] = metas.get("google-site-verification", "")
    rec["meta"] = {k: metas[k] for k in sorted(metas)}

    rec["canonical"] = ""
    rec["preload"] = []
    for m in LINK_RE.finditer(html):
        a = attrs(m.group(1))
        rel = (a.get("rel") or "").lower()
        if rel == "canonical":
            rec["canonical"] = a.get("href", "")
        if "preload" in rel:
            rec["preload"].append({"as": a.get("as", ""), "href": a.get("href", ""), "type": a.get("type", "")})

    robots = rec["robots"].lower()
    rec["indexable"] = "noindex" not in robots
    rec["title_length"] = len(rec["title"])
    rec["description_length"] = len(rec["description"])
    rec["canonical_absolute"] = rec["canonical"].startswith("http://") or rec["canonical"].startswith("https://")
    rec["canonical_self"] = rec["canonical"].rstrip("/") == url.rstrip("/") or rec["canonical"] == url
    rec["canonical_matches_url"] = rec["canonical"] == url

    parser = PageHTML()
    try:
        parser.feed(html)
        parser.close()
    except Exception as e:
        rec["parse_error"] = str(e)

    rec["h1"] = parser.h1
    rec["h1_count"] = len(parser.h1)
    rec["headings"] = parser.headings
    rec["heading_skips"] = heading_skips(parser.headings)
    rec["faq"] = parser.faqs
    rec["faq_count"] = len(parser.faqs)
    rec["breadcrumb_html"] = parser.breadcrumb_html
    rec["table_count"] = parser.tables
    rec["ol_count"] = parser.ols
    rec["ul_count"] = parser.uls
    rec["data_prerendered"] = parser.data_prerendered
    rec["image_count"] = len(parser.imgs)
    rec["images"] = parser.imgs
    rec["image_sources"] = [i.get("src", "") for i in parser.imgs]
    rec["picture_count"] = parser.picture_count
    rec["source_tags"] = parser.sources

    main_text = WS_RE.sub(" ", "".join(parser.main_parts)).strip()
    if not main_text:
        main_text = WS_RE.sub(" ", "".join(parser.body_parts)).strip()
    rec["visible_text"] = main_text
    rec["word_count"] = len(words(main_text))
    rec["paragraphs"] = parser.paras
    rec["paragraph_word_counts"] = [len(words(p)) for p in parser.paras]
    rec["max_paragraph_words"] = max(rec["paragraph_word_counts"], default=0)
    rec["passages_80_160"] = sum(1 for n in rec["paragraph_word_counts"] if 80 <= n <= 160)
    rec["eeat_block_present"] = EEAT_FINGERPRINT in html
    rec["answer_first"] = bool(parser.h1) and (bool(parser.paras) or rec["word_count"] > 40)

    internal = []
    external = []
    for a in parser.anchors:
        href = a["href"]
        absu = absolutize(href, url)
        item = {"href": href, "abs": absu, "rel": a["rel"], "text": a["text"][:120]}
        if is_internal(href):
            internal.append(item)
        elif href and not href.startswith(("mailto:", "tel:", "javascript:", "#")):
            external.append(item)
    rec["internal_links"] = [x["abs"] for x in internal]
    rec["internal_link_objects"] = internal
    rec["internal_link_count"] = len(internal)
    rec["external_link_count"] = len(external)
    rec["external_links"] = external

    blocks = parse_ld_blocks(html)
    rec["structured_data"] = [
        {"index": b["index"], "parse_ok": b["parse_ok"], "error": b["error"], "data": b["data"]} for b in blocks
    ]
    rec["jsonld_raw"] = [b["raw"] for b in blocks]
    ld = ld_summary(blocks, url)
    rec.update({f"ld_{k}" if not k.startswith("ld_") else k: v for k, v in []})
    rec["schema"] = ld
    rec["schema_types"] = ld["schema_types"]
    rec["jsonld_parse_ok"] = ld["parse_ok"]

    rec["h2_br_raw"] = []
    for m in BR_H2_RE.finditer(html):
        inner = m.group(1)
        if "<br" in inner.lower():
            rec["h2_br_raw"].append(inner)

    md = url_to_md(url)
    rec["md_twin_exists"] = md.is_file()
    rec["md_twin_bytes"] = md.stat().st_size if md.is_file() else 0
    rec["md_twin_words"] = len(words(md.read_text(encoding="utf-8"))) if md.is_file() else 0
    rec["md_twin_ratio"] = (rec["md_twin_words"] / rec["word_count"]) if rec["word_count"] else None

    rec["has_hours_html"] = bool(
        re.search(r"Pazartesi|opening|çalışma saat|09:00|10:00", html, re.I)
    )
    rec["has_maps_link"] = "google.com/maps" in html or "maps.app.goo.gl" in html
    rec["has_phone"] = bool(re.search(r"\+90\s*5|0552|tel:", html))
    rec["has_address"] = "Süleymanpaşa" in html or "Tekirdağ" in html
    rec["footer_legal_href"] = any(p in html for p in LEGAL_PATHS)
    rec["og_alt_stale"] = "Yaratıcı Ajans" in rec.get("og_image_alt", "")
    rec["h2_concat_sektorler"] = bool(re.search(r"Çalıştığımız<br\s*/?>Sektörler", html, re.I))
    rec["h2_concat_bilgi"] = bool(re.search(r"Bilgi<br\s*/?>Merkezi", html, re.I))
    return rec


def image_bytes_for_page(rec: dict[str, Any]) -> dict[str, Any]:
    jpeg_bytes = 0
    webp_bytes = 0
    files = []
    try:
        from PIL import Image
    except Exception:
        Image = None  # type: ignore
    for img in rec.get("images") or []:
        src = img.get("src") or ""
        if not src.startswith("/"):
            continue
        p = ROOT / src.lstrip("/")
        item = {
            "src": src,
            "exists": p.is_file(),
            "bytes": p.stat().st_size if p.is_file() else None,
            "ext": p.suffix.lower(),
            "width_attr": img.get("width"),
            "height_attr": img.get("height"),
            "loading": img.get("loading"),
            "in_picture": img.get("in_picture"),
            "file_width": None,
            "file_height": None,
        }
        if p.is_file() and Image is not None:
            try:
                with Image.open(p) as im:
                    item["file_width"], item["file_height"] = im.size
            except Exception:
                pass
        if p.suffix.lower() in {".jpg", ".jpeg"} and p.is_file():
            jpeg_bytes += p.stat().st_size
        files.append(item)
    webp_from_source = []
    for src in rec.get("source_tags") or []:
        if "webp" not in (src.get("type") or "") and ".webp" not in (src.get("srcset") or ""):
            continue
        for token in (src.get("srcset") or "").split(","):
            u = token.strip().split(" ")[0]
            if not u:
                continue
            p = ROOT / u.lstrip("/")
            wb = p.stat().st_size if p.is_file() else None
            webp_from_source.append({"srcset": u, "bytes": wb, "exists": p.is_file()})
            if wb:
                webp_bytes += wb
    return {
        "jpeg_fallback_bytes": jpeg_bytes,
        "webp_source_bytes": webp_bytes,
        "picture_count": rec.get("picture_count", 0),
        "img_count": rec.get("image_count", 0),
        "files": files,
        "webp_sources": webp_from_source,
        "lazy_imgs": sum(1 for i in rec.get("images") or [] if i.get("loading") == "lazy"),
        "preload_images": [p for p in rec.get("preload") or [] if p.get("as") == "image"],
        "browser_selected_bytes": None,
        "browser_selected_note": "HAR/Lighthouse not run. JPEG vs WebP are disk sizes of referenced files, not transfer.",
    }


def parse_sitemap() -> dict[str, Any]:
    p = ROOT / "sitemap.xml"
    text = p.read_text(encoding="utf-8") if p.is_file() else ""
    locs = re.findall(r"<loc>(.*?)</loc>", text)
    lastmods = re.findall(r"<url>(.*?)</url>", text, re.S)
    rows = []
    for block in lastmods:
        loc_m = re.search(r"<loc>(.*?)</loc>", block)
        lm = re.search(r"<lastmod>(.*?)</lastmod>", block)
        if loc_m:
            rows.append({"loc": loc_m.group(1), "lastmod": lm.group(1) if lm else None})
    return {
        "exists": p.is_file(),
        "bytes": p.stat().st_size if p.is_file() else 0,
        "url_count": len(locs),
        "locs": locs,
        "rows": rows,
        "missing_lastmod": [r["loc"] for r in rows if not r["lastmod"]],
        "invalid_loc": [u for u in locs if not u.startswith("https://")],
        "duplicate_locs": [u for u, n in Counter(locs).items() if n > 1],
        "private_locs": [
            u
            for u in locs
            if "/admin/" in u or "/proje/" in u or "404.html" in u or u.rstrip("/").endswith("/404")
        ],
    }


def parse_robots_git() -> dict[str, Any]:
    p = ROOT / "robots.txt"
    text = p.read_text(encoding="utf-8") if p.is_file() else ""
    sitemap_decl = re.findall(r"(?i)^sitemap:\s*(\S+)", text, re.M)
    return {
        "exists": p.is_file(),
        "text": text,
        "sitemap_declaration": sitemap_decl,
        "disallow_admin": "Disallow: /admin/" in text,
        "disallow_proje": "Disallow: /proje/" in text,
        "mentions_gptbot": "GPTBot" in text,
    }


def fetch_live(url: str, timeout: int = 15) -> dict[str, Any]:
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "malt-seo-benchmark/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            return {
                "ok": True,
                "status": resp.status,
                "final_url": resp.geturl(),
                "headers": {k.lower(): v for k, v in resp.headers.items()},
                "body": body.decode("utf-8", errors="replace"),
                "bytes": len(body),
            }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def probe_redirect(url: str, timeout: int = 12) -> dict[str, Any]:
    hops = []
    current = url
    for _ in range(6):
        req = urllib.request.Request(current, method="GET", headers={"User-Agent": "malt-seo-benchmark/1.0"})
        try:
            opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
            # manual to count hops
        except Exception:
            pass
        class NoRedir(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None

        opener = urllib.request.build_opener(NoRedir)
        try:
            resp = opener.open(req, timeout=timeout)
            hops.append({"url": current, "status": getattr(resp, "status", 200), "location": None})
            break
        except urllib.error.HTTPError as e:
            loc = e.headers.get("Location") if e.headers else None
            hops.append({"url": current, "status": e.code, "location": loc})
            if e.code in (301, 302, 303, 307, 308) and loc:
                current = urljoin(current, loc)
                continue
            break
        except Exception as e:
            hops.append({"url": current, "status": 0, "error": str(e)})
            break
    return {"start": url, "hops": hops, "chain_length": max(0, len(hops) - 1)}


def build_crawl(pages: list[dict[str, Any]], rules: list[dict[str, str]], corpus: set[str]) -> dict[str, Any]:
    by_url = {p["url"]: p for p in pages}
    graph = {p["url"]: [] for p in pages}
    broken = []
    redirect_hits = []
    gone = []
    for page in pages:
        seen = set()
        for item in page.get("internal_link_objects") or []:
            absu = item["abs"]
            parsed = urlparse(absu)
            path = parsed.path or "/"
            page_url = normalize_page_url(f"{SITE}{path}" if parsed.path else absu)
            if parsed.fragment and path in ("", "/"):
                page_url = HOME
            dest = page_url
            if dest not in seen:
                graph[page["url"]].append(dest)
                seen.add(dest)
            if dest in corpus:
                continue
            # hash-only home
            if parsed.fragment and (path in ("", "/")):
                continue
            rule = match_redirect(path, rules)
            if rule:
                entry = {"from_page": page["url"], "href": absu, "rule": rule}
                if rule["status"] == "410":
                    gone.append(entry)
                else:
                    redirect_hits.append(entry)
                continue
            if path.startswith("/admin/") or path.startswith("/proje/"):
                continue
            if path.startswith("/#") or path == "/":
                continue
            if not local_exists(dest) and dest not in corpus:
                # maybe file without trailing slash
                if not local_exists(absu.split("#")[0]):
                    broken.append({"from": page["url"], "href": absu, "path": path})

    # BFS depth from homepage
    depth = {HOME: 0}
    q = deque([HOME])
    while q:
        cur = q.popleft()
        for nxt in graph.get(cur, []):
            if nxt not in corpus:
                continue
            if nxt not in depth:
                depth[nxt] = depth[cur] + 1
                q.append(nxt)

    inbound = defaultdict(int)
    for src, dests in graph.items():
        for d in dests:
            if d in corpus and d != src:
                inbound[d] += 1

    orphans = []
    for u in sorted(corpus):
        if u == HOME:
            continue
        if u not in depth:
            orphans.append(
                {
                    "url": u,
                    "inbound_from_corpus": inbound[u],
                    "classification": "unreachable_from_homepage_in_corpus_graph",
                    "not": "true_global_orphan",
                }
            )
        elif inbound[u] == 0:
            orphans.append(
                {
                    "url": u,
                    "inbound_from_corpus": 0,
                    "classification": "no_inbound_from_other_corpus_pages",
                    "not": "true_global_orphan",
                }
            )

    return {
        "graph": graph,
        "depth_from_home": depth,
        "unreachable_from_home": [u for u in sorted(corpus) if u not in depth],
        "orphan_candidates_in_corpus": orphans,
        "broken_internal": broken,
        "redirect_follow_from_corpus": redirect_hits,
        "gone_links": gone,
        "note": "Orphans are corpus-graph only. Partial-site claims are not made.",
    }


def score_geo(rec: dict[str, Any], shared: dict[str, Any]) -> dict[str, Any]:
    ld = rec.get("schema") or {}
    evidence: dict[str, list[str]] = {}
    scores: dict[str, int] = {}

    # Entity clarity
    nap_html = rec.get("has_phone") and rec.get("has_address")
    has_lb = ld.get("has_localbusiness")
    geo = ld.get("has_geo")
    hours = ld.get("has_hours")
    logo = ld.get("has_logo_or_image")
    same = ld.get("sameAs") or []
    gbp = any("g.page" in str(x) or "business.google" in str(x) or "maps/place" in str(x) for x in same)
    if not rec.get("title") and not nap_html:
        scores["entity_clarity"] = 0
        evidence["entity_clarity"] = ["No title/NAP"]
    elif not nap_html:
        scores["entity_clarity"] = 1
        evidence["entity_clarity"] = ["Brand/title only"]
    elif has_lb and geo and hours and logo and gbp:
        scores["entity_clarity"] = 5
        evidence["entity_clarity"] = ["LocalBusiness + geo/hours/logo + GBP/sameAs"]
    elif has_lb and geo and hours and logo:
        scores["entity_clarity"] = 4
        evidence["entity_clarity"] = ["LocalBusiness + geo/hours/logo"]
    elif has_lb and nap_html:
        missing = [k for k, v in (("geo", geo), ("hours", hours), ("logo", logo)) if not v]
        scores["entity_clarity"] = 3
        evidence["entity_clarity"] = [
            f"LocalBusiness present; NAP in HTML; schema missing: {missing}; sameAs={same}"
        ]
    else:
        scores["entity_clarity"] = 2
        evidence["entity_clarity"] = [
            f"NAP in HTML (phone={rec.get('has_phone')} address={rec.get('has_address')}); LocalBusiness={has_lb}"
        ]

    # Answerability
    faq = rec.get("faq") or []
    max_ans = max((f.get("a_words") or 0) for f in faq) if faq else 0
    passages = rec.get("passages_80_160") or 0
    if rec.get("table_count", 0) and passages:
        scores["answerability"] = 5
        evidence["answerability"] = [f"table={rec['table_count']} passages_80_160={passages}"]
    elif passages:
        scores["answerability"] = 4
        evidence["answerability"] = [f"passages_80_160={passages} max_p={rec.get('max_paragraph_words')}"]
    elif faq and max_ans >= 25:
        scores["answerability"] = 3
        evidence["answerability"] = [f"FAQ n={len(faq)} max_answer_words={max_ans}"]
    elif faq:
        scores["answerability"] = 2
        q0 = faq[0]["q"][:80] if faq else ""
        evidence["answerability"] = [f"FAQ n={len(faq)} max_answer_words={max_ans} sample={q0!r}"]
    elif rec.get("word_count", 0) > 80:
        scores["answerability"] = 1
        evidence["answerability"] = [f"No FAQ; word_count={rec.get('word_count')}"]
    else:
        scores["answerability"] = 0
        evidence["answerability"] = ["No FAQ / thin"]

    # Semantic structure
    h1n = rec.get("h1_count") or 0
    skips = rec.get("heading_skips") or []
    question_h2 = sum(1 for h in rec.get("headings") or [] if h["tag"] == "h2" and h["text"].endswith("?"))
    if h1n == 0:
        scores["semantic_structure"] = 0
        evidence["semantic_structure"] = ["No H1"]
    elif h1n > 1:
        scores["semantic_structure"] = 1
        evidence["semantic_structure"] = [f"H1 count={h1n}"]
    elif rec.get("table_count", 0) and question_h2:
        scores["semantic_structure"] = 5
        evidence["semantic_structure"] = ["H1 + question H2 + table"]
    elif question_h2 and rec.get("ol_count", 0):
        scores["semantic_structure"] = 4
        evidence["semantic_structure"] = [f"question_h2={question_h2} ol={rec.get('ol_count')}"]
    elif h1n == 1 and not skips and rec.get("ul_count", 0):
        scores["semantic_structure"] = 3
        evidence["semantic_structure"] = [f"1 H1, no skips, lists ul={rec.get('ul_count')} ol={rec.get('ol_count')}"]
    elif h1n == 1:
        scores["semantic_structure"] = 2
        evidence["semantic_structure"] = [f"1 H1; skips={skips[:3]}"]
    else:
        scores["semantic_structure"] = 1
        evidence["semantic_structure"] = ["Weak heading tree"]

    # Structured data
    types = ld.get("schema_types") or []
    if rec.get("jsonld_parse_ok") is False:
        scores["structured_data"] = 1
        evidence["structured_data"] = [f"parse failures {ld.get('parse_failures')}"]
    elif not types:
        scores["structured_data"] = 0
        evidence["structured_data"] = ["No JSON-LD"]
    elif (
        ld.get("has_website_node")
        and ld.get("has_faqpage")
        and (ld.get("has_article") or ld.get("has_service"))
        and not ld.get("dangling_refs")
        and ld.get("knowsAbout")
    ):
        scores["structured_data"] = 5
        evidence["structured_data"] = [f"types={types}"]
    elif ld.get("has_faqpage") and (ld.get("has_article") or ld.get("has_website_node")):
        scores["structured_data"] = 4
        evidence["structured_data"] = [f"FAQPage+Article/WebSite types={types}"]
    elif ld.get("has_website_node") and ld.get("has_service") and ld.get("has_breadcrumb_list"):
        scores["structured_data"] = 3
        evidence["structured_data"] = [f"WebSite+Service+Breadcrumb types={types}"]
    elif ld.get("has_service") and ld.get("has_breadcrumb_list"):
        scores["structured_data"] = 2
        evidence["structured_data"] = [
            f"Service+Breadcrumb; website_node={ld.get('has_website_node')} dangling={ld.get('dangling_refs')}"
        ]
    elif ld.get("has_localbusiness"):
        scores["structured_data"] = 2
        evidence["structured_data"] = [
            f"Thin LocalBusiness types={types} geo={geo} hours={hours} website={ld.get('has_website_node')}"
        ]
    else:
        scores["structured_data"] = 2
        evidence["structured_data"] = [f"types={types} dangling={ld.get('dangling_refs')}"]

    # Machine readability
    twin_ok = rec.get("md_twin_exists")
    ratio = rec.get("md_twin_ratio")
    llms = shared.get("llms_exists")
    bots_blocked = shared.get("live_bots_blocked")
    if rec.get("word_count", 0) < 20:
        scores["machine_readability"] = 1
        evidence["machine_readability"] = ["Thin HTML"]
    elif llms and twin_ok and ratio is not None and ratio >= 0.7 and bots_blocked is False:
        scores["machine_readability"] = 5
        evidence["machine_readability"] = [f"twins ratio={ratio:.2f}; bots not blocked"]
    elif llms and twin_ok and ratio is not None and ratio >= 0.7:
        scores["machine_readability"] = 4
        evidence["machine_readability"] = [f"llms+twin ratio={ratio:.2f}; live bot block={bots_blocked}"]
    elif llms and twin_ok:
        scores["machine_readability"] = 3
        evidence["machine_readability"] = [f"llms+twin exists ratio={ratio}; prerender={rec.get('data_prerendered')}"]
    else:
        scores["machine_readability"] = 2
        evidence["machine_readability"] = [f"SSR words={rec.get('word_count')} twin={twin_ok} llms={llms}"]

    # Entity relationships
    if ld.get("has_website_node") and ld.get("has_service") and same and gbp:
        scores["entity_relationships"] = 5
        evidence["entity_relationships"] = ["WebSite hub + GBP sameAs"]
    elif ld.get("has_website_node") and (ld.get("has_service") or ld.get("ispartof_website")):
        scores["entity_relationships"] = 4
        evidence["entity_relationships"] = ["WebSite hub present"]
    elif ld.get("has_breadcrumb_list") and rec.get("schema_types"):
        scores["entity_relationships"] = 3
        evidence["entity_relationships"] = [
            f"BreadcrumbList; isPartOf website={ld.get('ispartof_website')} dangling={ld.get('dangling_refs')}"
        ]
    elif rec.get("breadcrumb_html"):
        scores["entity_relationships"] = 2
        evidence["entity_relationships"] = ["HTML breadcrumb, no/weak schema links"]
    elif rec.get("internal_link_count", 0) > 3:
        scores["entity_relationships"] = 1
        evidence["entity_relationships"] = [f"links={rec.get('internal_link_count')} no breadcrumb schema"]
    else:
        scores["entity_relationships"] = 0
        evidence["entity_relationships"] = ["Isolated"]

    # Trust
    legal = shared.get("legal_url_exists")
    if rec.get("has_phone") and rec.get("has_address") and rec.get("has_hours_html") and rec.get("has_maps_link") and legal:
        scores["trust"] = 4
        evidence["trust"] = ["NAP+hours+maps+legal"]
    elif rec.get("has_hours_html") and rec.get("has_maps_link") and nap_html:
        scores["trust"] = 3
        evidence["trust"] = ["NAP + hours/maps HTML"]
    elif nap_html:
        scores["trust"] = 2
        evidence["trust"] = [f"NAP HTML; legal={legal} hours_html={rec.get('has_hours_html')} maps={rec.get('has_maps_link')}"]
    elif rec.get("has_phone") or rec.get("has_address"):
        scores["trust"] = 1
        evidence["trust"] = ["Partial contact"]
    else:
        scores["trust"] = 0
        evidence["trust"] = ["No contact"]

    # Freshness
    sm = shared.get("sitemap") or {}
    lastmod = None
    for row in sm.get("rows") or []:
        if row["loc"].rstrip("/") == rec["url"].rstrip("/"):
            lastmod = row.get("lastmod")
    missing_ratio = len(sm.get("missing_lastmod") or []) / max(sm.get("url_count") or 1, 1)
    if rec.get("schema", {}).get("has_article") and lastmod:
        scores["freshness"] = 4
        evidence["freshness"] = [f"Article + lastmod={lastmod}"]
    elif lastmod and missing_ratio == 0:
        scores["freshness"] = 3
        evidence["freshness"] = [f"lastmod={lastmod}; all sitemap URLs dated"]
    elif lastmod:
        scores["freshness"] = 2
        evidence["freshness"] = [f"lastmod={lastmod}; sitemap missing lastmod n={len(sm.get('missing_lastmod') or [])}"]
    else:
        scores["freshness"] = 1
        evidence["freshness"] = [f"No lastmod on this URL; copyright-only fallback"]

    # Extractability
    eeat = rec.get("eeat_block_present")
    if rec["url"].startswith(f"{SITE}/projeler/") and rec.get("word_count", 0) >= 400 and not eeat:
        scores["extractability"] = 5
        evidence["extractability"] = [f"project words={rec.get('word_count')} unique"]
    elif passages and not eeat:
        scores["extractability"] = 4
        evidence["extractability"] = [f"80–160w passages={passages}"]
    elif rec.get("max_paragraph_words", 0) >= 40:
        scores["extractability"] = 3
        evidence["extractability"] = [
            f"max_p={rec.get('max_paragraph_words')} words={rec.get('word_count')} eeat_clone={eeat}"
        ]
    elif rec.get("word_count", 0) >= 80:
        scores["extractability"] = 2
        evidence["extractability"] = [f"short/cards words={rec.get('word_count')} eeat={eeat}"]
    elif rec.get("word_count", 0) > 0:
        scores["extractability"] = 1
        evidence["extractability"] = [f"fragments words={rec.get('word_count')}"]
    else:
        scores["extractability"] = 0
        evidence["extractability"] = ["Nothing quotable"]

    mean = sum(scores.values()) / 9
    return {
        "url": rec["url"],
        "scores": scores,
        "mean": round(mean, 3),
        "evidence": evidence,
        "rubric": "seo/benchmark/geo-rubric.md",
    }


def finding_checks(pages: list[dict[str, Any]], shared: dict[str, Any]) -> list[dict[str, Any]]:
    by = {p["url"]: p for p in pages}
    home = by.get(HOME) or {}
    tabela = by.get(f"{SITE}/hizmetler/tabela/") or {}
    guide = by.get(f"{SITE}/bilgi/tabela-cesitleri/") or {}
    ofiso = by.get(f"{SITE}/projeler/ofiso/") or {}
    home_ld = home.get("schema") or {}
    checks = []

    def add(fid, metric, value, passed, detail):
        checks.append(
            {
                "finding_id": fid,
                "metric": metric,
                "value": value,
                "pass": passed,
                "detail": detail,
            }
        )

    add(
        "SCHEMA-001",
        "home_ld_has_website",
        home_ld.get("has_website_node"),
        bool(home_ld.get("has_website_node")),
        f"types={home_ld.get('schema_types')}",
    )
    add(
        "SCHEMA-001",
        "home_ld_geo",
        home_ld.get("has_geo"),
        bool(home_ld.get("has_geo")),
        "geo on #business",
    )
    add("SCHEMA-001", "home_ld_hours", home_ld.get("has_hours"), bool(home_ld.get("has_hours")), "")
    add("SCHEMA-001", "home_ld_logo", home_ld.get("has_logo_or_image"), bool(home_ld.get("has_logo_or_image")), "")
    add(
        "SCHEMA-001",
        "home_ld_knowsAbout_ge3",
        len(home_ld.get("knowsAbout") or []),
        len(home_ld.get("knowsAbout") or []) >= 3,
        str(home_ld.get("knowsAbout")),
    )
    add(
        "LOCAL-002",
        "home_ld_geo_hours",
        {"geo": home_ld.get("has_geo"), "hours": home_ld.get("has_hours")},
        bool(home_ld.get("has_geo") and home_ld.get("has_hours")),
        "same patch as SCHEMA-001",
    )
    add(
        "SCHEMA-002",
        "inner_isPartOf_website_id",
        (tabela.get("schema") or {}).get("ispartof_website"),
        bool((tabela.get("schema") or {}).get("ispartof_website")),
        f"dangling={ (tabela.get('schema') or {}).get('dangling_refs') }",
    )
    add(
        "SCHEMA-002",
        "website_node_defined_on_home",
        home_ld.get("has_website_node"),
        bool(home_ld.get("has_website_node")),
        "inner refs require homepage definition",
    )
    faq_html_n = home.get("faq_count") or 0
    add(
        "SCHEMA-003",
        "faqpage_parity_home",
        {"html_faq": faq_html_n, "faqpage": home_ld.get("has_faqpage")},
        bool(home_ld.get("has_faqpage")) and faq_html_n > 0,
        "FAQPage must match visible details",
    )
    add(
        "SCHEMA-003",
        "faqpage_parity_tabela",
        {
            "html_faq": tabela.get("faq_count"),
            "faqpage": (tabela.get("schema") or {}).get("has_faqpage"),
        },
        bool((tabela.get("schema") or {}).get("has_faqpage")),
        "",
    )
    info_pages = [p for p in pages if "/bilgi/" in p["url"] or "/sektorler/" in p["url"]]
    missing_ld = [p["url"] for p in info_pages if not p.get("schema_types")]
    add("SCHEMA-004", "guides_sectors_have_jsonld", len(missing_ld) == 0, len(missing_ld) == 0, missing_ld)
    add(
        "SCHEMA-005",
        "sameAs",
        home_ld.get("sameAs"),
        any("instagram.com/maltstudio.co" in str(u) for u in (home_ld.get("sameAs") or []))
        and not any("linkedin.com/company/malt-studio" in str(u) for u in (home_ld.get("sameAs") or [])),
        "Instagram required from CMS; Jakarta LinkedIn must stay absent",
    )
    live_robots = (shared.get("live_robots") or {}).get("body") or ""
    blocked = [ua for ua in BOT_AGENTS if ua in live_robots and "Disallow: /" in live_robots]
    add(
        "TECHSEO-001",
        "live_robots_blocks_ai",
        blocked,
        len(blocked) == 0,
        "pass = GPTBot/ClaudeBot/Google-Extended not Disallow / on live",
    )
    git_robots = shared.get("robots_git") or {}
    add(
        "TECHSEO-001",
        "git_robots_keeps_admin_proje",
        {"admin": git_robots.get("disallow_admin"), "proje": git_robots.get("disallow_proje")},
        bool(git_robots.get("disallow_admin") and git_robots.get("disallow_proje")),
        "git robots must keep private paths",
    )
    sm = shared.get("sitemap") or {}
    add(
        "TECHSEO-002",
        "sitemap_all_lastmod",
        len(sm.get("missing_lastmod") or []),
        len(sm.get("missing_lastmod") or []) == 0,
        sm.get("missing_lastmod"),
    )
    required_sitemap = [p["url"] for p in pages] + [f"{SITE}/gizlilik/", f"{SITE}/hakkimizda/"]
    locs = sm.get("locs") or []
    missing_required = [u for u in required_sitemap if u not in locs]
    private_locs = sm.get("private_locs") or []
    dup_locs = sm.get("duplicate_locs") or []
    invalid_locs = sm.get("invalid_loc") or []
    add(
        "TECHSEO-002",
        "sitemap_required_public",
        missing_required,
        len(missing_required) == 0,
        "frozen corpus + /gizlilik/ + /hakkimizda/ must appear; count is not frozen",
    )
    add("TECHSEO-002", "sitemap_unique", dup_locs, len(dup_locs) == 0, dup_locs)
    add("TECHSEO-002", "sitemap_no_private", private_locs, len(private_locs) == 0, private_locs)
    add(
        "TECHSEO-002",
        "sitemap_absolute_https",
        invalid_locs,
        len(invalid_locs) == 0,
        invalid_locs,
    )
    add(
        "TECHSEO-002",
        "sitemap_url_count",
        sm.get("url_count"),
        len(locs) >= len(required_sitemap) and not missing_required and not dup_locs and not private_locs,
        f"required={len(required_sitemap)} listed={len(locs)}",
    )
    add(
        "TECHSEO-005",
        "gsc_meta",
        home.get("gsc_verification"),
        bool(home.get("gsc_verification")),
        "empty expected BEFORE",
    )
    add(
        "SEO-001",
        "og_image_alt_not_stale",
        home.get("og_image_alt"),
        not home.get("og_alt_stale"),
        home.get("og_image_alt"),
    )
    add(
        "SEO-002",
        "h2_br_space_sektorler",
        home.get("h2_concat_sektorler"),
        not home.get("h2_concat_sektorler"),
        "Çalıştığımız<br>Sektörler concat",
    )
    add("SEO-002", "h2_br_space_bilgi", home.get("h2_concat_bilgi"), not home.get("h2_concat_bilgi"), "")
    add("SEO-003", "iletisim_not_required", True, True, "canonical contact is /bolgeler/tekirdag/")
    imgs = home.get("images") or []
    work = [i for i in imgs if "work-swatch" in (i.get("class") or "")]
    first_lazy = work[0]["loading"] == "lazy" if work else None
    add("PERF-001", "picture_webp_home", home.get("picture_count", 0) > 0, home.get("picture_count", 0) > 0, "")
    add(
        "PERF-002",
        "first_work_img_lazy",
        first_lazy,
        first_lazy is False,
        "first work-item img loading attr",
    )
    proj = [p for p in pages if p["url"].startswith(f"{SITE}/projeler/") and p["url"] != f"{SITE}/projeler/"]
    min_wc = min((p.get("word_count") or 0) for p in proj) if proj else 0
    add("CONTENT-001", "project_wordcount_min", min_wc, min_wc >= 400, {p["url"]: p.get("word_count") for p in proj})
    eeat_files = [p["url"] for p in pages if p.get("eeat_block_present")]
    add("CONTENT-002", "eeat_clone_pages", len(eeat_files), len(eeat_files) <= 2, eeat_files)
    add(
        "CONTENT-003",
        "guide_passage_80_160",
        guide.get("passages_80_160"),
        (guide.get("passages_80_160") or 0) >= 1,
        f"max_p={guide.get('max_paragraph_words')}",
    )
    isikli = by.get(f"{SITE}/bilgi/isikli-mi-isiksiz-mi/") or {}
    add("CONTENT-003", "comparison_table", isikli.get("table_count"), (isikli.get("table_count") or 0) >= 1, "")
    hakkimizda = (ROOT / "hakkimizda" / "index.html").is_file()
    add("CONTENT-004", "about_page", hakkimizda, hakkimizda, "absence is trust gap, not crawl bug")
    legal = shared.get("legal_url_exists")
    add("CONTENT-005", "kvkk_or_privacy", legal, bool(legal), shared.get("legal_paths_found"))
    add("GEO-001", "llms_txt_exists", shared.get("llms_exists"), bool(shared.get("llms_exists")), "")
    add(
        "GEO-002",
        "md_twin_ratio_home",
        home.get("md_twin_ratio"),
        (home.get("md_twin_ratio") or 0) >= 0.70,
        f"md={home.get('md_twin_words')} html={home.get('word_count')}",
    )
    has_map = any("hasMap" in str(x) for x in home_ld.get("important_properties") or [])
    add(
        "LOCAL-001",
        "hasMap",
        has_map,
        has_map,
        "CMS googleMapsUrl coordinate search; not a GBP Place ID",
    )
    add("LOCAL-001", "gbp_place_id", None, None, "EXTERNAL GBP not measured here")
    add(
        "BRAND-001",
        "cms_linkedin_empty",
        shared.get("cms_linkedin"),
        shared.get("cms_linkedin") in ("", None),
        "do not add Jakarta slug",
    )
    add("EXTERNAL-001", "serp_not_collected", None, None, "EXTERNAL — no local rank claim")
    titles = [p.get("title") for p in pages if p.get("title")]
    dup_t = [t for t, n in Counter(titles).items() if n > 1]
    add("SEO-META", "duplicate_titles", dup_t, len(dup_t) == 0, dup_t)
    descs = [p.get("description") for p in pages if p.get("description")]
    dup_d = [t for t, n in Counter(descs).items() if n > 1]
    add("SEO-META", "duplicate_descriptions", dup_d, len(dup_d) == 0, dup_d)
    add("TECHSEO-META", "title_home_nonempty", home.get("title_length"), 20 <= (home.get("title_length") or 0) <= 70, home.get("title"))
    add("TECHSEO-META", "h1_count_home", home.get("h1_count"), home.get("h1_count") == 1, home.get("h1"))
    add("TECHSEO-META", "canonical_home_self", home.get("canonical"), home.get("canonical") == HOME, home.get("canonical"))
    add(
        "SCHEMA-PARSE",
        "jsonld_parse_ok",
        all(p.get("jsonld_parse_ok") for p in pages),
        all(p.get("jsonld_parse_ok") for p in pages),
        [p["url"] for p in pages if not p.get("jsonld_parse_ok")],
    )
    return checks


def dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_report(ctx: dict[str, Any]) -> str:
    checks = ctx["checks"]
    geo = ctx["geo"]
    fails = [c for c in checks if c["pass"] is False]
    geo_mean = round(sum(g["mean"] for g in geo) / len(geo), 3) if geo else None
    phase = ctx.get("phase") or "BEFORE"
    lines = [
        f"# GEO/SEO {phase} capture",
        "",
        f"- **{phase} SHA:** `{ctx['git']['sha']}`",
        f"- **Branch:** `{ctx['git']['branch']}`",
        f"- **Benchmark date:** {ctx['captured_at']}",
        f"- **Python:** {ctx['env']['python']}",
        f"- **Pillow:** {ctx['env'].get('Pillow')}",
        f"- **Chrome:** {ctx['env'].get('chrome_binary')}",
        f"- **Lighthouse:** {ctx['env'].get('lighthouse')}",
        f"- **Config hash:** `{ctx['config_hash']}`",
        "",
        "## Methodology",
        "",
        "- Parser reads **built HTML on disk** (not a JS DOM).",
        "- JSON-LD from `<script type=\"application/ld+json\">` via `json.loads`.",
        "- URL corpus: `seo/benchmark/urls.txt` (35 sitemap URLs).",
        "- GEO queries: `seo/benchmark/geo-queries.json` (observational only; no rank/citation claims).",
        "- GEO rubric: `seo/benchmark/geo-rubric.md` (Stage 2 frozen 0–5, nine dimensions).",
        "- Performance runtime (LCP/CLS/HAR-selected bytes) **not collected** — Lighthouse not installed; not added.",
        "",
        "## Exact URL corpus",
        "",
    ]
    for u in ctx["urls"]:
        lines.append(f"- {u}")
    lines += [
        "",
        "## Metric definitions",
        "",
        "- `word_count`: whitespace-split tokens in `<main>` (header/footer/nav excluded).",
        "- `indexable`: robots meta does not contain `noindex`.",
        "- `orphan candidate`: unreachable from homepage **inside this 35-URL graph** — not a global orphan.",
        "- Image JPEG/WebP bytes: **on-disk** sizes of referenced files. Browser-selected transfer is unmeasured.",
        "",
        f"## GEO proxy (five-URL mean): **{geo_mean}** / 5",
        "",
        "| URL | entity | answer | semantic | schema | machine | relations | trust | freshness | extract | mean |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    keys = [
        "entity_clarity",
        "answerability",
        "semantic_structure",
        "structured_data",
        "machine_readability",
        "entity_relationships",
        "trust",
        "freshness",
        "extractability",
    ]
    for g in geo:
        s = g["scores"]
        lines.append(
            "| `"
            + url_path(g["url"])
            + "` | "
            + " | ".join(str(s[k]) for k in keys)
            + f" | {g['mean']} |"
        )
    lines += ["", f"## Deterministic checks (fail = current {phase} gap)", ""]
    for c in fails:
        lines.append(f"- **{c['finding_id']}** `{c['metric']}` = `{c['value']}` — {c['detail']}")
    lines += ["", "## Performance", "", "Runtime Lighthouse/HAR: **not measured** (see `performance/`). Disk image evidence:"]
    perf = ctx["performance"]
    home_img = perf.get("home_images") or {}
    lines += [
        f"- Homepage JPEG fallback bytes (disk): {home_img.get('jpeg_fallback_bytes')}",
        f"- Homepage WebP source bytes (disk): {home_img.get('webp_source_bytes')}",
        f"- Homepage `<picture>` count: {home_img.get('picture_count')}",
        "",
        "## Sitemap / robots",
        "",
        f"- Git robots.txt exists: {ctx['robots_git']['exists']}; sitemap decl: {ctx['robots_git']['sitemap_declaration']}",
        f"- Live robots fetched: {ctx['live_robots'].get('ok')} status={ctx['live_robots'].get('status')}",
        f"- Live AI bot Disallow / agents: {ctx['live_bots_blocked_agents']}",
        f"- Sitemap locs: {ctx['sitemap']['url_count']}; missing lastmod: {len(ctx['sitemap']['missing_lastmod'])}",
        "",
        "## Crawl (corpus graph)",
        "",
        f"- Broken internal (sample): {len(ctx['crawl']['broken_internal'])}",
        f"- Unreachable from homepage in corpus: {ctx['crawl']['unreachable_from_home']}",
        f"- Redirect rules hit from corpus links: {len(ctx['crawl']['redirect_follow_from_corpus'])}",
        "",
        "## External metrics unavailable locally",
        "",
        "- LOCAL-001 GBP listing",
        "- BRAND-001 LinkedIn entity (Jakarta collision) — not scraped",
        "- EXTERNAL-001 SERP position",
        "- ChatGPT / Perplexity / Gemini / AIO citations",
        "- Lighthouse LCP/CLS/TBT and HAR-selected image bytes",
        "",
        "## Known limitations",
        "",
        "- Live HTTP timings are noise; not a scorecard.",
        "- `www` redirect chain (TECHSEO-003) recorded only if probes succeeded.",
        "- Python 3.9.6 local vs Cloudflare build 3.11 — parse results are encoding-stable JSON/HTML.",
        "",
        "## Finding ID map",
        "",
        "Every check row carries `finding_id`. GEO scores apply to SCHEMA-*, CONTENT-*, GEO-001/002, LOCAL-002.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="GEO/SEO collector. Does not mutate the site.")
    parser.add_argument(
        "--out",
        default="artifacts/geo-seo/before",
        help="Artifact directory relative to repo root (default: artifacts/geo-seo/before)",
    )
    parser.add_argument("--phase", choices=("BEFORE", "AFTER"), default=None)
    args = parser.parse_args(argv)
    global OUT
    OUT = Path(args.out)
    if not OUT.is_absolute():
        OUT = ROOT / OUT
    phase = args.phase or ("AFTER" if OUT.name == "after" else "BEFORE")

    urls = load_urls()
    if len(urls) != 35:
        print(f"collect: expected 35 URLs, got {len(urls)}", file=sys.stderr)
        return 1
    captured_at = now_iso()
    git = git_state()
    env = pkg_versions()
    cfg = sha256_text(
        (BENCH / "urls.txt").read_text(encoding="utf-8"),
        (BENCH / "geo-queries.json").read_text(encoding="utf-8"),
        (BENCH / "geo-rubric.md").read_text(encoding="utf-8"),
    )
    queries = json.loads((BENCH / "geo-queries.json").read_text(encoding="utf-8"))
    sitemap = parse_sitemap()
    robots_git = parse_robots_git()
    rules = parse_redirects()
    cms_linkedin = ""
    try:
        cms = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
        cms_linkedin = cms.get("linkedin") or ""
    except Exception:
        cms = {}

    pages = [parse_page(u) for u in urls]
    missing_files = [p["url"] for p in pages if p.get("status") != 200]

    for d in ("urls", "metadata", "schema", "links", "crawl", "geo", "performance", "raw"):
        (OUT / d).mkdir(parents=True, exist_ok=True)

    images_by_url = {p["url"]: image_bytes_for_page(p) for p in pages}

    live_robots = fetch_live(f"{SITE}/robots.txt")
    live_body = live_robots.get("body") or ""
    live_bots_blocked_agents = []
    if live_robots.get("ok"):
        # CF managed robots often prepend per-agent Disallow /
        for ua in BOT_AGENTS:
            block = re.search(rf"(?is)User-agent:\s*{re.escape(ua)}\s+Disallow:\s*/\s", live_body)
            if block:
                live_bots_blocked_agents.append(ua)

    legal_found = [p for p in LEGAL_PATHS if (ROOT / p.strip("/") / "index.html").is_file()]
    llms_exists = (ROOT / "llms.txt").is_file()
    llms_txt = (ROOT / "llms.txt").read_text(encoding="utf-8") if llms_exists else ""

    shared = {
        "llms_exists": llms_exists,
        "llms_has_h1": llms_txt.startswith("# ") if llms_txt else False,
        "sitemap": sitemap,
        "live_bots_blocked": bool(live_bots_blocked_agents),
        "legal_url_exists": bool(legal_found),
        "legal_paths_found": legal_found,
        "cms_linkedin": cms_linkedin,
        "live_robots": {k: v for k, v in live_robots.items() if k != "body"},
        "robots_git": robots_git,
    }

    geo = [score_geo(by, shared) for by in pages if by["url"] in GEO_SCORE_URLS]
    # keep frozen order
    geo.sort(key=lambda g: GEO_SCORE_URLS.index(g["url"]))

    crawl = build_crawl(pages, rules, set(urls))
    checks = finding_checks(pages, {**shared, "live_robots": live_robots})

    redirect_probes = []
    for probe in (
        HOME,
        f"{SITE}/hizmetler/tabela",
        "https://www.maltstudio.co/",
        f"{SITE}/iletisim/",
    ):
        redirect_probes.append(probe_redirect(probe))

    # metadata aggregates
    titles = Counter(p.get("title") for p in pages)
    descs = Counter(p.get("description") for p in pages)
    metadata = {
        "title_presence": sum(1 for p in pages if p.get("title")),
        "description_presence": sum(1 for p in pages if p.get("description")),
        "canonical_presence": sum(1 for p in pages if p.get("canonical")),
        "canonical_absolute": sum(1 for p in pages if p.get("canonical_absolute")),
        "canonical_self": sum(1 for p in pages if p.get("canonical_matches_url")),
        "duplicate_titles": [t for t, n in titles.items() if t and n > 1],
        "duplicate_descriptions": [t for t, n in descs.items() if t and n > 1],
        "og_title": sum(1 for p in pages if p.get("og_title")),
        "og_description": sum(1 for p in pages if p.get("og_description")),
        "og_image": sum(1 for p in pages if p.get("og_image")),
        "og_image_alt": sum(1 for p in pages if p.get("og_image_alt")),
        "twitter_card": sum(1 for p in pages if p.get("twitter_card")),
        "pages": [
            {
                "url": p["url"],
                "title": p.get("title"),
                "title_length": p.get("title_length"),
                "description": p.get("description"),
                "description_length": p.get("description_length"),
                "canonical": p.get("canonical"),
                "canonical_absolute": p.get("canonical_absolute"),
                "canonical_matches_url": p.get("canonical_matches_url"),
                "robots": p.get("robots"),
                "og_title": p.get("og_title"),
                "og_description": p.get("og_description"),
                "og_image": p.get("og_image"),
                "og_image_alt": p.get("og_image_alt"),
                "twitter_title": p.get("twitter_title"),
                "twitter_description": p.get("twitter_description"),
                "twitter_image": p.get("twitter_image"),
                "twitter_image_alt": p.get("twitter_image_alt"),
                "indexable": p.get("indexable"),
            }
            for p in pages
        ],
    }

    schema_out = {
        "pages": [
            {
                "url": p["url"],
                "schema_types": p.get("schema_types"),
                "schema": p.get("schema"),
                "jsonld_parse_ok": p.get("jsonld_parse_ok"),
                "structured_data": p.get("structured_data"),
            }
            for p in pages
        ]
    }

    home_images = images_by_url.get(HOME) or {}
    performance = {
        "status": "runtime_not_collected",
        "reason": "Lighthouse CLI is not installed. Node toolchain was not added. Chrome binary exists but HAR was not captured.",
        "captured_at": captured_at,
        "home_images": home_images,
        "first_work_img_lazy": next(
            (i.get("loading") == "lazy" for i in (next(p for p in pages if p["url"] == HOME).get("images") or []) if "work-swatch" in (i.get("class") or "")),
            None,
        ),
        "redirect_probes": redirect_probes,
        "runs": [],
        "median_note": "Fewer than 3 Lighthouse runs; no median.",
    }

    summary = {
        "phase": phase,
        "captured_at": captured_at,
        "git": {"branch": git["branch"], "sha": git["sha"]},
        "env": env,
        "config_hash": cfg,
        "url_count": len(urls),
        "urls_missing_html": missing_files,
        "geo_mean": round(sum(g["mean"] for g in geo) / len(geo), 3) if geo else None,
        "geo_by_url": {g["url"]: g["mean"] for g in geo},
        "failing_checks": [c for c in checks if c["pass"] is False],
        "passing_checks": [c for c in checks if c["pass"] is True],
        "unscored_external": [c for c in checks if c["pass"] is None],
        "sitemap_url_count": sitemap["url_count"],
        "jsonld_parse_ok": all(p.get("jsonld_parse_ok") for p in pages),
        "live_robots_ok": live_robots.get("ok"),
        "live_bots_blocked_agents": live_bots_blocked_agents,
    }

    ctx = {
        "phase": phase,
        "captured_at": captured_at,
        "git": git,
        "env": env,
        "config_hash": cfg,
        "urls": urls,
        "checks": checks,
        "geo": geo,
        "performance": performance,
        "robots_git": robots_git,
        "live_robots": live_robots,
        "live_bots_blocked_agents": live_bots_blocked_agents,
        "sitemap": sitemap,
        "crawl": crawl,
    }
    report = write_report(ctx)

    # per-url
    for p in pages:
        slug = url_slug(p["url"])
        slim = {k: v for k, v in p.items() if k not in ("jsonld_raw", "visible_text")}
        slim["images_measured"] = images_by_url[p["url"]]
        dump(OUT / "urls" / f"{slug}.json", slim)
        dump(OUT / "schema" / f"{slug}.json", {"url": p["url"], "schema": p.get("schema"), "blocks": p.get("structured_data")})

    dump(OUT / "summary.json", summary)
    dump(OUT / "metadata" / "aggregate.json", metadata)
    dump(OUT / "schema" / "aggregate.json", schema_out)
    dump(OUT / "links" / "graph.json", {k: v for k, v in crawl.items() if k != "note"})
    dump(OUT / "crawl" / "graph.json", crawl)
    dump(OUT / "geo" / "scores.json", {"rubric": "seo/benchmark/geo-rubric.md", "urls": geo, "mean": summary["geo_mean"]})
    dump(OUT / "geo" / "queries.json", queries)
    (OUT / "geo" / "rubric.md").write_text((BENCH / "geo-rubric.md").read_text(encoding="utf-8"), encoding="utf-8")
    dump(OUT / "performance" / "baseline.json", performance)
    dump(OUT / "raw" / "git-state.json", git)
    dump(OUT / "raw" / "env.json", env)
    dump(OUT / "raw" / "checks.json", checks)
    (OUT / "raw" / "robots-git.txt").write_text(robots_git.get("text") or "", encoding="utf-8")
    if live_robots.get("ok"):
        (OUT / "raw" / "robots-live.txt").write_text(live_body, encoding="utf-8")
    else:
        dump(OUT / "raw" / "robots-live-error.json", live_robots)
    dump(OUT / "raw" / "sitemap.json", sitemap)
    dump(OUT / "raw" / "redirect-probes.json", redirect_probes)
    dump(OUT / "raw" / "cms-linkedin.json", {"linkedin": cms_linkedin})
    (OUT / "report.md").write_text(report, encoding="utf-8")

    expected = [
        OUT / "summary.json",
        OUT / "report.md",
        OUT / "metadata" / "aggregate.json",
        OUT / "schema" / "aggregate.json",
        OUT / "crawl" / "graph.json",
        OUT / "geo" / "scores.json",
        OUT / "performance" / "baseline.json",
    ]
    missing_art = [str(p.relative_to(ROOT)) for p in expected if not p.is_file()]
    url_arts = list((OUT / "urls").glob("*.json"))
    validation = {
        "all_urls_tested": len(pages) == 35 and not missing_files,
        "url_artifact_count": len(url_arts),
        "json_ok": True,
        "jsonld_parse_completed": all(p.get("jsonld_parse_ok") for p in pages),
        "metadata_completed": True,
        "crawl_generated": bool(crawl.get("graph")),
        "geo_rubric_applied": len(geo) == 5,
        "performance_labeled": performance["status"] == "runtime_not_collected",
        "missing_artifacts": missing_art,
        "missing_html": missing_files,
    }
    dump(OUT / "raw" / "validation.json", validation)

    print(f"{phase} captured SHA={git['sha']} urls={len(pages)} geo_mean={summary['geo_mean']} fails={len(summary['failing_checks'])}")
    if missing_files or missing_art:
        print("collect: incomplete", missing_files, missing_art, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
