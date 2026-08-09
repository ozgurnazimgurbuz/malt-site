#!/usr/bin/env python3
"""Resize/compress portfolio uploads for card display without quality collapse.

CMS may upload phone-resolution JPEGs (2–5MB, 2000–5000px). Work-grid cards
display at ~4:5 and rarely need more than ~1200 CSS pixels wide (retina).

For each image under images/uploads/:
  - Cap the long edge at CARD_MAX (default 1200)
  - Rewrite progressive JPEG in place (q≈82) when oversized
  - Emit a sibling .webp (q≈80) for <picture> / srcset consumers

Idempotent: already-card-sized JPEGs are not re-encoded; missing WebP is added.
Run from Netlify build (before prerender) and locally after CMS media uploads.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
UPLOADS = ROOT / "images" / "uploads"

# Card / grid targets. Portrait phone shots are object-fit:cover in 4:5 tiles,
# so width (not the long edge) drives sharpness on retina phones.
CARD_MAX_W = 1200
CARD_MAX_H = 1800
JPEG_QUALITY = 82
WEBP_QUALITY = 80

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def load_rgb(path: Path) -> Image.Image:
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    # MPO / HEIC-ish multi-frame phone dumps: keep first frame only.
    if getattr(im, "n_frames", 1) > 1:
        im.seek(0)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (20, 16, 16))
        bg.paste(im, mask=im.split()[-1])
        return bg
    if im.mode != "RGB":
        return im.convert("RGB")
    return im


def fit_card(
    im: Image.Image, max_w: int = CARD_MAX_W, max_h: int = CARD_MAX_H
) -> Image.Image:
    w, h = im.size
    scale = min(1.0, max_w / float(w), max_h / float(h))
    if scale >= 0.999:
        return im
    nw = max(1, int(round(w * scale)))
    nh = max(1, int(round(h * scale)))
    return im.resize((nw, nh), Image.Resampling.LANCZOS)


def webp_path_for(src: Path) -> Path:
    return src.with_suffix(".webp")


def save_jpeg(im: Image.Image, path: Path) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    im.save(
        tmp,
        format="JPEG",
        quality=JPEG_QUALITY,
        optimize=True,
        progressive=True,
        subsampling=1,  # 4:2:2 — sharper than 4:2:0 for signage text
    )
    tmp.replace(path)


def save_webp(im: Image.Image, path: Path) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    im.save(
        tmp,
        format="WEBP",
        quality=WEBP_QUALITY,
        method=6,
    )
    tmp.replace(path)


def process_one(path: Path) -> dict:
    before = path.stat().st_size
    im = load_rgb(path)
    ow, oh = im.size
    fitted = fit_card(im)
    nw, nh = fitted.size
    webp = webp_path_for(path)

    resized = (nw, nh) != (ow, oh)
    wrote_jpeg = False

    # Never re-encode an already-card-sized JPEG (generation loss on every deploy).
    # Only rewrite when dimensions exceed the card box.
    if path.suffix.lower() in {".jpg", ".jpeg"} and resized:
        save_jpeg(fitted, path)
        wrote_jpeg = True
    elif path.suffix.lower() == ".png" and resized:
        # PNG photo cards: resize in place; WebP sibling still emitted.
        fitted.save(path, format="PNG", optimize=True)
        wrote_jpeg = True

    after_jpeg = path.stat().st_size
    need_webp = (not webp.exists()) or wrote_jpeg or resized
    if need_webp:
        # Re-load from the (possibly rewritten) raster we will serve.
        if wrote_jpeg and path.suffix.lower() in {".jpg", ".jpeg"}:
            base = load_rgb(path)
        else:
            base = fitted
        save_webp(base, webp)

    after_webp = webp.stat().st_size if webp.exists() else 0
    return {
        "name": path.name,
        "before_kb": before / 1024,
        "after_kb": after_jpeg / 1024,
        "webp_kb": after_webp / 1024,
        "from": f"{ow}x{oh}",
        "to": f"{nw}x{nh}",
        "wrote_jpeg": wrote_jpeg,
        "webp": webp.name,
    }


def main() -> int:
    if not UPLOADS.is_dir():
        print(f"optimize_uploads: missing {UPLOADS}", file=sys.stderr)
        return 1

    rows = []
    for path in sorted(UPLOADS.iterdir()):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        if path.suffix.lower() not in IMAGE_EXTS:
            continue
        # WebP siblings are outputs, not sources (unless orphaned).
        if path.suffix.lower() == ".webp":
            continue
        try:
            rows.append(process_one(path))
        except Exception as exc:  # noqa: BLE001 — keep build going; report failure
            print(f"optimize_uploads: FAIL {path.name}: {exc}", file=sys.stderr)
            return 1

    if not rows:
        print("optimize_uploads: no images")
        return 0

    total_before = sum(r["before_kb"] for r in rows)
    total_after = sum(r["after_kb"] for r in rows)
    total_webp = sum(r["webp_kb"] for r in rows)
    for r in rows:
        flag = "rewrote" if r["wrote_jpeg"] else "kept"
        print(
            f"  {r['name']}: {r['before_kb']:.0f}KB → {r['after_kb']:.0f}KB JPEG "
            f"+ {r['webp_kb']:.0f}KB WebP  {r['from']} → {r['to']}  ({flag})"
        )
    print(
        f"optimize_uploads: {len(rows)} files, "
        f"JPEG {total_before:.0f}KB → {total_after:.0f}KB "
        f"({100 * (1 - total_after / total_before):.0f}% smaller), "
        f"WebP total {total_webp:.0f}KB"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
