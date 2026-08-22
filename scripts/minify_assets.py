#!/usr/bin/env python3
"""Minify shared production assets in-place for Netlify deploy.

Readable sources stay in Git; this runs as the last build step so the
published artifact is minified. Fails the build on any error.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ASSETS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "assets/site.css",
        "css",
        (":root{", "[data-theme=", "@media", ".track-"),
    ),
    (
        "assets/liquid-glass.css",
        "css",
        ("html.liquid-glass", "[data-theme=", "@supports", "backdrop-filter"),
    ),
    (
        "assets/theme.js",
        "js",
        ("malt-theme", "liquid-glass", "data-theme-toggle", "localStorage"),
    ),
)


def _minify_css(src: str) -> str:
    import rcssmin  # noqa: WPS433 — runtime dep, optional until build

    return rcssmin.cssmin(src, keep_bang_comments=False)


def _minify_js(src: str) -> str:
    import rjsmin  # noqa: WPS433

    return rjsmin.jsmin(src)


def _check_markers(label: str, out: str, markers: tuple[str, ...]) -> None:
    missing = [m for m in markers if m not in out]
    if missing:
        raise ValueError(f"{label}: missing after minify: {', '.join(missing)}")


def main() -> int:
    rows: list[tuple[str, int, int]] = []

    for rel, kind, markers in ASSETS:
        path = ROOT / rel
        if not path.is_file():
            print(f"minify_assets: FAIL missing {rel}", file=sys.stderr)
            return 1

        src = path.read_text(encoding="utf-8")
        before = len(src.encode("utf-8"))

        try:
            out = _minify_css(src) if kind == "css" else _minify_js(src)
        except Exception as exc:
            print(f"minify_assets: FAIL {rel}: {exc}", file=sys.stderr)
            return 1

        if not out or not out.strip():
            print(f"minify_assets: FAIL {rel}: empty output", file=sys.stderr)
            return 1

        try:
            _check_markers(rel, out, markers)
        except ValueError as exc:
            print(f"minify_assets: FAIL {exc}", file=sys.stderr)
            return 1

        path.write_text(out if out.endswith("\n") else out + "\n", encoding="utf-8")
        after = len(out.encode("utf-8"))
        rows.append((rel, before, after))
        pct = (1 - after / before) * 100 if before else 0.0
        print(f"minify_assets: {rel} {before} -> {after} bytes ({pct:.1f}% smaller)")

    print("minify_assets: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
