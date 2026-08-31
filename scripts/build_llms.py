#!/usr/bin/env python3
"""Generate AI-agent discovery files (llms.txt) and Markdown twins for every public page.

Follows https://llmstxt.org/:
  - /llms.txt curated index at site root
  - /llms-full.txt concatenated Markdown of all public pages
  - For each HTML page, a twin at the same path with .md appended
    (directory URLs → index.html.md)

Does NOT add .md URLs to sitemap.xml (sitemap stays frozen for Google).
Google AI Overviews do not use llms.txt; this is for third-party agents.
"""
from __future__ import annotations

import html as html_lib
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://maltstudio.co"
SITEMAP = ROOT / "sitemap.xml"


# ---------------------------------------------------------------------------
# HTML → Markdown
# ---------------------------------------------------------------------------


class _MdConverter(HTMLParser):
    """Convert selected main-content HTML into readable Markdown."""

    SKIP_TAGS = {
        "script",
        "style",
        "noscript",
        "svg",
        "header",
        "footer",
        "nav",
        "form",
    }
    BLOCK = {"p", "div", "section", "article", "li", "h1", "h2", "h3", "h4", "blockquote", "tr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0
        self._in_a = 0
        self._a_href = ""
        self._a_text: list[str] = []
        self._li_ordered_depth = 0
        self._list_stack: list[str] = []  # "ul" | "ol"
        self._ol_counters: list[int] = []
        self._pending_space = False
        self._in_cell = False
        self._cell_parts: list[str] = []
        self._table_row: list[str] = []
        self._table_header_emitted = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = {k: (v or "") for k, v in attrs}
        if tag in self.SKIP_TAGS:
            self._skip += 1
            return
        if self._skip:
            return
        if tag in ("h1", "h2", "h3", "h4"):
            if self._in_a:
                self._a_text.append(" ")
            else:
                level = int(tag[1])
                self._flush_inline()
                self.parts.append("\n\n" + "#" * level + " ")
        elif tag == "p":
            if self._in_a:
                self._a_text.append(" ")
            else:
                self._flush_inline()
                self.parts.append("\n\n")
        elif tag == "div":
            if self._in_a:
                self._a_text.append(" ")
        elif tag == "br":
            if self._in_a:
                self._a_text.append(" ")
            else:
                self.parts.append(" ")
        elif tag == "li":
            self._flush_inline()
            kind = self._list_stack[-1] if self._list_stack else "ul"
            if kind == "ol":
                self._ol_counters[-1] += 1
                n = self._ol_counters[-1]
                self.parts.append(f"\n{n}. ")
            else:
                self.parts.append("\n- ")
        elif tag == "ul":
            self._flush_inline()
            self._list_stack.append("ul")
        elif tag == "ol":
            self._flush_inline()
            self._list_stack.append("ol")
            self._ol_counters.append(0)
        elif tag in ("strong", "b"):
            self.parts.append("**")
        elif tag in ("em", "i"):
            self.parts.append("*")
        elif tag == "a":
            self._in_a += 1
            if self._in_a == 1:
                self._a_href = ad.get("href", "")
                self._a_text = []
        elif tag == "blockquote":
            self._flush_inline()
            self.parts.append("\n\n> ")
        elif tag == "table":
            self._flush_inline()
            self.parts.append("\n\n")
            self._table_header_emitted = False
        elif tag == "tr":
            self._flush_inline()
            self._table_row = []
        elif tag in ("td", "th"):
            self._flush_inline()
            self._in_cell = True
            self._cell_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS:
            if self._skip:
                self._skip -= 1
            return
        if self._skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "p", "blockquote"):
            if self._in_a:
                self._a_text.append(" ")
            else:
                self._flush_inline()
                self.parts.append("\n")
        elif tag == "li":
            self._flush_inline()
        elif tag == "ul":
            if self._list_stack and self._list_stack[-1] == "ul":
                self._list_stack.pop()
            self.parts.append("\n")
        elif tag == "ol":
            if self._list_stack and self._list_stack[-1] == "ol":
                self._list_stack.pop()
            if self._ol_counters:
                self._ol_counters.pop()
            self.parts.append("\n")
        elif tag in ("strong", "b"):
            self.parts.append("**")
        elif tag in ("em", "i"):
            self.parts.append("*")
        elif tag == "a":
            if self._in_a == 1:
                text = re.sub(r"\s+", " ", "".join(self._a_text)).strip() or self._a_href
                href = self._abs_href(self._a_href)
                if href and text:
                    md = f"[{text}]({href})"
                    if self._in_cell:
                        self._cell_parts.append(md)
                    else:
                        self.parts.append(md)
                        self.parts.append(" ")
                elif text:
                    if self._in_cell:
                        self._cell_parts.append(text)
                    else:
                        self.parts.append(text)
                self._a_text = []
                self._a_href = ""
            if self._in_a:
                self._in_a -= 1
        elif tag in ("td", "th"):
            cell = re.sub(r"\s+", " ", "".join(self._cell_parts)).strip()
            self._table_row.append(cell.replace("|", "\\|"))
            self._in_cell = False
            self._cell_parts = []
        elif tag == "tr":
            if self._table_row:
                self.parts.append("| " + " | ".join(self._table_row) + " |\n")
                if not self._table_header_emitted:
                    self.parts.append("| " + " | ".join("---" for _ in self._table_row) + " |\n")
                    self._table_header_emitted = True
            self._table_row = []
        elif tag == "table":
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip:
            return
        text = re.sub(r"[ \t\r\n]+", " ", data)
        if not text or text.isspace():
            return
        if self._in_a:
            self._a_text.append(text)
            return
        if self._in_cell:
            if self._cell_parts and not self._cell_parts[-1].endswith((" ", "[", "(", "/")):
                if not text.startswith((" ", ",", ".", ";", ":", "!", "?", ")", "]")):
                    self._cell_parts.append(" ")
            self._cell_parts.append(text)
            return
        if self.parts and not self.parts[-1].endswith(("\n", " ", "[", "(", "*", ">")):
            if not text.startswith((" ", ",", ".", ";", ":", "!", "?", ")", "]")):
                self.parts.append(" ")
        self.parts.append(text)

    def _flush_inline(self) -> None:
        pass

    @staticmethod
    def _abs_href(href: str) -> str:
        href = (href or "").strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            return href
        if href.startswith("//"):
            return "https:" + href
        if href.startswith("/"):
            return SITE + href
        return href

    def get_markdown(self) -> str:
        raw = "".join(self.parts)
        raw = html_lib.unescape(raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        raw = re.sub(r"[ \t]+\n", "\n", raw)
        return raw.strip() + "\n"


def meta(html: str, name: str) -> str:
    m = re.search(
        rf'<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\']([^"\']*)["\']',
        html,
        re.I,
    )
    if m:
        return html_lib.unescape(m.group(1).strip())
    m = re.search(
        rf'<meta\s+content=["\']([^"\']*)["\']\s+name=["\']{re.escape(name)}["\']',
        html,
        re.I,
    )
    return html_lib.unescape(m.group(1).strip()) if m else ""


def title_tag(html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    return html_lib.unescape(re.sub(r"\s+", " ", m.group(1)).strip()) if m else ""


def canonical(html: str) -> str:
    m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',
        html,
        re.I,
    )
    return m.group(1).strip() if m else ""


def extract_main_html(doc: str) -> str:
    """Prefer page-main / hero content; fall back to <body> without chrome."""
    chunks: list[str] = []
    for pattern in (
        r'(<section\s+class="page-hero"[^>]*>.*?</section>)',
        r'(<section\s+class="page-main"[^>]*>.*?</section>)',
        r'(<section\s+class="hero"[^>]*>.*?</section>)',
        r'(<section\s+class="[^"]*section-band[^"]*"[^>]*>.*?</section>)',
        r'(<section\s+class="cta"[^>]*>.*?</section>)',
        r'(<section\s+id="teklif"[^>]*>.*?</section>)',
        r'(<section\s+id="iletisim"[^>]*>.*?</section>)',
        r'(<section\s+class="trust-strip"[^>]*>.*?</section>)',
        r'(<section\s+class="services"[^>]*>.*?</section>)',
        r'(<section\s+aria-label="[^"]*"[^>]*>.*?</section>)',
    ):
        chunks.extend(re.findall(pattern, doc, flags=re.I | re.S))
    if chunks:
        # Deduplicate while preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for c in chunks:
            key = c[:200]
            if key in seen:
                continue
            seen.add(key)
            unique.append(c)
        return "\n".join(unique)

    body = re.search(r"<body[^>]*>(.*)</body>", doc, re.I | re.S)
    if not body:
        return doc
    text = body.group(1)
    text = re.sub(r"<header\b[^>]*>.*?</header>", "", text, flags=re.I | re.S)
    text = re.sub(r"<footer\b[^>]*>.*?</footer>", "", text, flags=re.I | re.S)
    text = re.sub(r"<nav\b[^>]*>.*?</nav>", "", text, flags=re.I | re.S)
    return text


def home_entity_stanza() -> str:
    """Main-content extract strips the footer; homepage twin still needs NAP."""
    c = load_contact()
    email = c.get("email") or "merhaba@maltstudio.co"
    phone = c.get("phone") or "05525826959"
    ig = (c.get("instagram") or "").strip()
    street = (c.get("addressStreet") or "Yavuz Mahallesi, Ruşen Güneş Sokak, D Blok No:2").strip()
    postal = (c.get("addressPostalCode") or "59100").strip()
    city = c.get("addressLocality") or "Süleymanpaşa"
    region = c.get("addressRegion") or "Tekirdağ"
    lines = [
        "## İletişim",
        f"- {email} · {phone} · +90 552 582 69 59",
        f"- {street}, {postal} {city}/{region}, Türkiye",
        "- Pazartesi–Cumartesi 09:00–19:00",
    ]
    if ig:
        lines.append(f"- Instagram: {ig}")
    return "\n".join(lines)


def html_to_markdown(doc: str, page_url: str) -> str:
    title = title_tag(doc)
    desc = meta(doc, "description")
    canon = canonical(doc) or page_url
    main = extract_main_html(doc)
    conv = _MdConverter()
    conv.feed(main)
    conv.close()
    body = conv.get_markdown()
    is_home = page_url.rstrip("/") in ("", SITE)
    entity = home_entity_stanza() if is_home else ""

    lines = [
        f"# {title}" if title else "# Malt Studio",
        "",
        f"> {desc}" if desc else "",
        "",
        f"- Canonical HTML: {canon}",
        f"- Markdown twin: {md_url_for(page_url)}",
        f"- Site: {SITE}/",
        "",
        "---",
        "",
        entity,
        body,
    ]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text


# ---------------------------------------------------------------------------
# Paths / sitemap
# ---------------------------------------------------------------------------


def sitemap_urls() -> list[str]:
    tree = ET.parse(SITEMAP)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [
        (el.text or "").strip()
        for el in tree.findall(".//sm:loc", ns)
        if (el.text or "").strip()
    ]
    if not urls:
        # fallback without namespace
        urls = [
            (el.text or "").strip()
            for el in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            if (el.text or "").strip()
        ]
    if not urls:
        urls = [(el.text or "").strip() for el in tree.findall(".//loc") if (el.text or "").strip()]
    return urls


def html_path_for(url: str) -> Path:
    path = url.replace(SITE, "").strip("/")
    if not path:
        return ROOT / "index.html"
    return ROOT / path / "index.html"


def md_path_for(url: str) -> Path:
    """llmstxt.org: append .md; directory URLs → index.html.md."""
    html_p = html_path_for(url)
    return html_p.with_name(html_p.name + ".md")  # index.html.md


def md_url_for(url: str) -> str:
    if url.rstrip("/") == SITE:
        return f"{SITE}/index.html.md"
    return url.rstrip("/") + "/index.html.md"


def page_title_from_md(md: str) -> str:
    m = re.match(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else "Sayfa"


def page_blurb_from_md(md: str) -> str:
    m = re.search(r"^>\s+(.+)$", md, re.M)
    if m:
        return m.group(1).strip()
    # first non-heading paragraph
    for line in md.splitlines():
        line = line.strip()
        if line and not line.startswith(("#", "-", ">", "---")):
            return line[:140].rstrip(".") + ("…" if len(line) > 140 else "")
    return "Malt Studio sayfası."


# ---------------------------------------------------------------------------
# Curated llms.txt
# ---------------------------------------------------------------------------


def load_contact() -> dict:
    path = ROOT / "content.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def section_of(url: str) -> str:
    path = url.replace(SITE, "")
    if path in ("/", ""):
        return "home"
    if path.startswith("/hizmet-bolge/"):
        return "local"
    if path.startswith("/hizmetler/"):
        return "services"
    if path.startswith("/bolgeler/"):
        return "local"
    if path.startswith("/sektorler/"):
        return "industries"
    if path.startswith("/bilgi/"):
        return "guides"
    if path.startswith("/projeler/"):
        return "projects"
    return "other"


def build_llms_txt(pages: list[tuple[str, str, str]]) -> str:
    """pages: (url, title, blurb) — HTML canonical URLs."""
    c = load_contact()
    email = c.get("email") or "merhaba@maltstudio.co"
    phone = c.get("phone") or "05525826959"
    city = c.get("addressLocality") or "Süleymanpaşa"
    region = c.get("addressRegion") or "Tekirdağ"
    ig = (c.get("instagram") or "").strip()
    street = (c.get("addressStreet") or "Yavuz Mahallesi, Ruşen Güneş Sokak, D Blok No:2").strip()
    postal = (c.get("addressPostalCode") or "59100").strip()

    by: dict[str, list[tuple[str, str, str]]] = {
        k: [] for k in ("home", "services", "local", "industries", "guides", "projects", "other")
    }
    for url, title, blurb in pages:
        by[section_of(url)].append((url, title, blurb))

    def link_lines(items: list[tuple[str, str, str]], hubs_first: bool = True) -> list[str]:
        def is_hub(u: str) -> bool:
            parts = [p for p in u.replace(SITE, "").strip("/").split("/") if p]
            return len(parts) <= 1

        ordered = sorted(items, key=lambda t: (0 if is_hub(t[0]) else 1, t[1].lower()))
        lines = []
        for url, title, blurb in ordered:
            md = md_url_for(url)
            note = blurb.replace("\n", " ").strip()
            if len(note) > 120:
                note = note[:117].rstrip() + "…"
            lines.append(f"- [{title}]({md}): {note}")
        return lines

    out: list[str] = [
        "# Malt Studio",
        f"> Tekirdağ merkezli reklam ajansı ve tabela üreticisi. Tabela, ışıklı tabela, kutu harf, totem, cam/araç giydirme, lightbox ve kurumsal kimlik — keşiften montaja.",
        "",
        "Bu dosya AI ajanları için küratörlü bir indekstir (https://llmstxt.org/).",
        "Her kamu sayfasının temiz Markdown ikizi vardır: HTML URL’sinin sonuna `.md` eklenir",
        f"(dizin URL’leri için `index.html.md`). Örnek: `{SITE}/hizmetler/tabela/index.html.md`.",
        "",
        "Önemli notlar:",
        f"- İletişim: {email} · {phone} · +90 552 582 69 59",
        f"- Adres: {street}, {postal} {city}/{region}, Türkiye",
        "- Çalışma saatleri: Pazartesi–Cumartesi 09:00–19:00",
        *([f"- Instagram: {ig}"] if ig else []),
        "- Teklif: keşif sonrası yazılı; internette sabit fiyat listesi yok",
        "- Uydurma şube/sertifika/metrik yazılmaz; kanıt proje sayfalarına bağlanır",
        f"- İnsan okuyan site haritası: {SITE}/sitemap.xml",
        f"- Tam birleşik Markdown: {SITE}/llms-full.txt",
        "",
        "## Ana sayfa",
        *link_lines(by["home"]),
        "",
        "## Hizmetler",
        *link_lines(by["services"]),
        "",
        "## Tekirdağ / yerel",
        *link_lines(by["local"]),
        "",
        "## Sektörler",
        *link_lines(by["industries"]),
        "",
        "## Bilgi rehberleri",
        *link_lines(by["guides"]),
        "",
        "## Projeler",
        *link_lines(by["projects"]),
        "",
        "## Optional",
        f"- [Sitemap]({SITE}/sitemap.xml): Arama motorları için HTML URL listesi (Markdown ikizleri dahil değil)",
        f"- [robots.txt]({SITE}/robots.txt): Tarama kuralları",
        f"- [content.json]({SITE}/content.json): CMS kaynak içerik (JSON)",
    ]
    if by["other"]:
        out += ["", "## Diğer", *link_lines(by["other"])]
    text = "\n".join(out).rstrip() + "\n"
    return text


def build_llms_full(md_docs: list[tuple[str, str]]) -> str:
    """Concatenate all page markdowns for agents that want one fetch."""
    chunks = [
        "# Malt Studio — full site Markdown",
        f"> Concatenated LLM-friendly exports of all public pages on {SITE}.",
        "",
        f"Source index: {SITE}/llms.txt",
        "",
    ]
    for url, md in md_docs:
        chunks.append(f"\n\n<!-- page: {url} -->\n\n")
        chunks.append(md.rstrip())
        chunks.append("\n")
    return "".join(chunks).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    urls = sitemap_urls()
    if not urls:
        raise SystemExit("build_llms: no URLs in sitemap.xml")

    pages_meta: list[tuple[str, str, str]] = []
    md_docs: list[tuple[str, str]] = []
    written = 0

    for url in urls:
        html_p = html_path_for(url)
        if not html_p.exists():
            print(f"build_llms: missing HTML for {url} → {html_p}")
            continue
        doc = html_p.read_text(encoding="utf-8")
        md = html_to_markdown(doc, url)
        md_p = md_path_for(url)
        md_p.parent.mkdir(parents=True, exist_ok=True)
        md_p.write_text(md, encoding="utf-8")
        written += 1
        title = page_title_from_md(md)
        blurb = page_blurb_from_md(md)
        pages_meta.append((url, title, blurb))
        md_docs.append((url, md))

    llms = build_llms_txt(pages_meta)
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8")
    full = build_llms_full(md_docs)
    (ROOT / "llms-full.txt").write_text(full, encoding="utf-8")

    print(f"build_llms: wrote {written} markdown twins")
    print(f"build_llms: llms.txt ({len(llms.encode('utf-8'))} bytes)")
    print(f"build_llms: llms-full.txt ({len(full.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
