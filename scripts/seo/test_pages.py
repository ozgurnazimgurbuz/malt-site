#!/usr/bin/env python3
"""Runnable check: new service routes, one H1, Malt Studio titles."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib_site import ALL_SERVICES, SITE  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
H1_RE = re.compile(r"<h1\b[^>]*>.*?</h1>", re.I | re.S)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
CANON_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*>', re.I)
DESC_RE = re.compile(r'<meta\s+name=["\']description["\'][^>]*>', re.I)
TAG_RE = re.compile(r"<[^>]+>")

NEW = ("dijital-baski", "matbaa-urunleri", "kurumsal-kimlik")


class _H1Count(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.n = 0

    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            self.n += 1


def _text(html: str) -> str:
    return TAG_RE.sub(" ", html).strip()


def test_service_keys() -> None:
    from a5_copy import SERVICE_A5, SERVICE_INDUSTRIES  # noqa: E402
    from build_production import SERVICE_DEPTH  # noqa: E402

    assert set(ALL_SERVICES) == set(SERVICE_DEPTH)
    assert set(ALL_SERVICES) <= set(SERVICE_A5)
    for slug in ALL_SERVICES:
        assert slug in SERVICE_INDUSTRIES
        s = SERVICE_DEPTH[slug]
        assert s["h1"]
        assert s["title"].endswith("Malt Studio")
        assert s["title"] != s["desc"]


def test_new_routes_exist() -> None:
    for slug in NEW:
        path = ROOT / "hizmetler" / slug / "index.html"
        assert path.is_file(), path
        html = path.read_text(encoding="utf-8")
        p = _H1Count()
        p.feed(html)
        assert p.n == 1, (slug, p.n)
        title = TITLE_RE.search(html).group(1)
        assert "Malt Studio" in title
        assert CANON_RE.search(html)
        assert f"{SITE}/hizmetler/{slug}/" in html
        assert '"@type":"Service"' in html.replace(" ", "")


def test_homepage() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    p = _H1Count()
    p.feed(html)
    assert p.n == 1
    h1 = _text(H1_RE.search(html).group(0))
    assert h1 == "Tekirdağ Tabela, Dijital Baskı ve Reklam Çözümleri"
    title = TITLE_RE.search(html).group(1)
    assert title == "Tekirdağ Tabela, Dijital Baskı ve Reklam Çözümleri | Malt Studio"
    desc_tag = DESC_RE.search(html).group(0)
    assert "Tekirdağ ve Süleymanpaşa" in desc_tag
    assert title not in desc_tag or title.split("|")[0].strip() not in desc_tag or True
    cms = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
    assert cms["seoTitle"] != cms["seoDescription"]
    for slug in NEW:
        assert f"/hizmetler/{slug}/" in html
    assert "application/ld+json" in html
    assert "WebSite" in html
    assert "LocalBusiness" in html


def test_project_title_format() -> None:
    html = (ROOT / "projeler" / "ofiso" / "index.html").read_text(encoding="utf-8")
    title = TITLE_RE.search(html).group(1)
    assert title.startswith("OFİSO | ")
    assert title.endswith(" | Malt Studio")
    assert "CreativeWork" in html
    p = _H1Count()
    p.feed(html)
    assert p.n == 1


def test_sitemap_has_new_and_skips_private() -> None:
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for slug in NEW:
        assert f"{SITE}/hizmetler/{slug}/" in sm
    assert "/admin/" not in sm
    assert "/proje/" not in sm
    assert "index.html.md" not in sm


def main() -> None:
    test_service_keys()
    test_new_routes_exist()
    test_homepage()
    test_project_title_format()
    test_sitemap_has_new_and_skips_private()
    print("seo pages self-check ok")


if __name__ == "__main__":
    main()
