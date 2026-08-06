#!/usr/bin/env python3
"""Simplify every page <header> nav to Teklif + İletişim only.

Does not touch breadcrumb nav (class="breadcrumb") or other navs.
Home uses #teklif / #iletisim; inner pages use /#teklif / /#iletisim.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HOME_NAV = """<nav aria-label="Ana menü">
    <a href="#teklif">Teklif</a>
    <a href="#iletisim">İletişim</a>
  </nav>"""

INNER_NAV = """<nav aria-label="Ana menü">
    <a href="/#teklif">Teklif</a>
    <a href="/#iletisim">İletişim</a>
  </nav>"""

HEADER_NAV_RE = re.compile(
    r"(<header\b[^>]*>[\s\S]*?)(<nav\b(?![^>]*breadcrumb)[^>]*>[\s\S]*?</nav>)",
    re.I,
)


def simplify_file(path: Path, *, home: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    nav = HOME_NAV if home else INNER_NAV

    def repl(m: re.Match) -> str:
        return m.group(1) + nav

    new, n = HEADER_NAV_RE.subn(repl, original, count=1)
    if n == 0:
        # fallback: first non-breadcrumb nav near top
        new2, n2 = re.subn(
            r"<nav\b(?![^>]*breadcrumb)[^>]*>[\s\S]*?</nav>",
            nav,
            original,
            count=1,
            flags=re.I,
        )
        if n2 == 0:
            print(f"skip (no header nav): {path.relative_to(ROOT)}")
            return False
        new = new2
    if new != original:
        path.write_text(new, encoding="utf-8")
        print(f"nav simplified: {path.relative_to(ROOT)}")
        return True
    print(f"unchanged: {path.relative_to(ROOT)}")
    return False


def main() -> int:
    changed = 0
    pages = [ROOT / "index.html"]
    for folder in (
        "hizmetler",
        "hizmet-bolge",
        "bolgeler",
        "projeler",
        "sektorler",
        "bilgi",
    ):
        pages.extend((ROOT / folder).rglob("index.html"))
    for path in sorted(set(pages)):
        if simplify_file(path, home=path.resolve() == (ROOT / "index.html").resolve()):
            changed += 1
    print(f"done: {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
