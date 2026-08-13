#!/usr/bin/env python3
"""Build private-ish customer project tracking pages at /proje/{slug}/.

Source: content/proje/*.json (Decap "Proje Takip" collection).
Never reads or writes content.json portfolio. Never adds URLs to sitemap.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_site import (  # noqa: E402
    PHONE_DISPLAY,
    PHONE_TEL,
    ROOT,
    SITE,
    footer,
    head,
    header,
    wa,
    write,
)

TRACK_DIR = ROOT / "content" / "proje"
OUT_DIR = ROOT / "proje"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

_TR_MONTHS = (
    "",
    "Ocak",
    "Şubat",
    "Mart",
    "Nisan",
    "Mayıs",
    "Haziran",
    "Temmuz",
    "Ağustos",
    "Eylül",
    "Ekim",
    "Kasım",
    "Aralık",
)


def _format_tr_date(raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        return ""
    # datetime widget may emit YYYY-MM-DD or ISO with time
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    if not m:
        return s
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if 1 <= mo <= 12:
        return f"{d} {_TR_MONTHS[mo]} {y}"
    return s


def _load_items() -> list[dict]:
    if not TRACK_DIR.is_dir():
        return []
    items: list[dict] = []
    for path in sorted(TRACK_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"track: skip {path.name}: {exc}")
            continue
        if not isinstance(data, dict):
            continue
        data["_source"] = path.name
        items.append(data)
    return items


def _normalize_steps(raw) -> list[dict]:
    out: list[dict] = []
    if not isinstance(raw, list):
        return out
    for step in raw:
        if not isinstance(step, dict):
            continue
        title = str(step.get("title") or "").strip()
        if not title:
            continue
        status = str(step.get("status") or "pending").strip().casefold()
        if status not in {"completed", "current", "pending"}:
            status = "pending"
        out.append(
            {
                "title": title,
                "description": str(step.get("description") or "").strip(),
                "status": status,
                "completedDate": str(step.get("completedDate") or "").strip(),
            }
        )
    return out


def _resolve_current(steps: list[dict], current_step: int | None) -> tuple[list[dict], int]:
    """Ensure exactly one current when possible; return 1-based index."""
    if not steps:
        return steps, 0
    currents = [i for i, s in enumerate(steps) if s["status"] == "current"]
    if len(currents) == 1:
        return steps, currents[0] + 1
    if current_step and 1 <= current_step <= len(steps):
        idx = current_step - 1
        for i, s in enumerate(steps):
            if i < idx:
                s["status"] = "completed"
            elif i == idx:
                s["status"] = "current"
            else:
                s["status"] = "pending"
        return steps, current_step
    # Fallback: first pending, else last
    for i, s in enumerate(steps):
        if s["status"] == "pending":
            s["status"] = "current"
            return steps, i + 1
    steps[-1]["status"] = "current"
    return steps, len(steps)


def _timeline_html(steps: list[dict]) -> str:
    items = []
    for s in steps:
        st = s["status"]
        mark = {"completed": "✓", "current": "●", "pending": "○"}[st]
        label = {"completed": "Tamamlandı", "current": "Şu an", "pending": "Bekliyor"}[st]
        desc = (
            f'<p class="track-step-desc">{html.escape(s["description"])}</p>'
            if s["description"]
            else ""
        )
        done = (
            f'<time class="track-step-date" datetime="{html.escape(s["completedDate"])}">'
            f"{html.escape(_format_tr_date(s['completedDate']))}</time>"
            if s["completedDate"]
            else ""
        )
        items.append(
            f'<li class="track-step track-step--{st}" data-status="{st}">'
            f'<span class="track-mark" aria-hidden="true">{mark}</span>'
            f'<div class="track-step-body">'
            f'<div class="track-step-title">{html.escape(s["title"])}</div>'
            f'<div class="track-step-status">{label}</div>'
            f"{desc}{done}"
            f"</div></li>"
        )
    return f'<ol class="track-timeline">{"".join(items)}</ol>'


def build_one(item: dict) -> str | None:
    """Write one page; return slug if written."""
    slug = str(item.get("slug") or "").strip().strip("/")
    if not slug or not SLUG_RE.fullmatch(slug):
        print(f"track: invalid slug in {item.get('_source')}: {slug!r}")
        return None
    if not item.get("public", True):
        return None

    project = str(item.get("projectName") or "").strip()
    client = str(item.get("clientName") or "").strip()
    if not project or not client:
        print(f"track: missing name fields for {slug}")
        return None

    steps = _normalize_steps(item.get("steps"))
    if not steps:
        print(f"track: no steps for {slug}")
        return None

    raw_cs = item.get("currentStep")
    try:
        cs = int(raw_cs) if raw_cs not in (None, "") else None
    except (TypeError, ValueError):
        cs = None
    steps, current_n = _resolve_current(steps, cs)
    current_title = steps[current_n - 1]["title"] if current_n else ""

    desc_raw = str(item.get("description") or "").strip()
    last_raw = str(item.get("lastUpdated") or "").strip()
    last_disp = _format_tr_date(last_raw)

    canonical = f"{SITE}/proje/{slug}/"
    title = f"{client} — Proje Durumu | Malt Studio"
    meta_desc = (
        f"{client} / {project} proje durumu."
        if not desc_raw
        else f"{client} — {desc_raw}."
    )

    cover = str(item.get("coverImage") or "").strip()
    cover_html = ""
    if cover:
        src = html.escape(cover)
        cover_html = (
            f'<div class="track-cover"><img src="{src}" alt="" '
            f'width="800" height="500" decoding="async"></div>'
        )

    last_html = (
        f'<p class="track-updated">Son güncelleme: '
        f'<time datetime="{html.escape(last_raw[:10] if last_raw else "")}">'
        f"{html.escape(last_disp)}</time></p>"
        if last_disp
        else ""
    )

    wa_msg = f"Merhaba, {client} / {project} projesi hakkında sorum var."
    page = f"""{head(
        html.escape(title),
        html.escape(meta_desc),
        canonical,
        noindex=True,
        nofollow=True,
    )}
<body class="track-page">
{header()}
<article class="track-study">
<section class="page-hero track-hero">
  <div class="wrap track-wrap">
    <div class="eyebrow">Malt Studio</div>
    <p class="track-client">{html.escape(client)}</p>
    <h1>{html.escape(project)}</h1>
    {f'<p class="lede">{html.escape(desc_raw)}</p>' if desc_raw else ""}
    {cover_html}
  </div>
</section>
<section class="page-main track-main">
  <div class="wrap track-wrap">
    <h2 class="track-status-heading">Proje durumu</h2>
    {_timeline_html(steps)}
    <div class="track-now" role="status">
      <div class="track-now-label">Şu anda</div>
      <p class="track-now-text">{html.escape(current_title)} aşamasındayız.</p>
      {last_html}
    </div>
  </div>
</section>
<section class="cta-band track-cta" aria-labelledby="track-cta-title">
  <div class="wrap">
    <h2 id="track-cta-title">Projenizle ilgili bir sorunuz mu var?</h2>
    <div class="cta-actions" style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
      <a class="btn btn-primary" href="{wa(wa_msg)}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>
</article>
{footer()}
</body></html>
"""
    write(OUT_DIR / slug / "index.html", page)
    return slug


def sync_orphan_dirs(keep: set[str]) -> None:
    """Remove /proje/{slug}/ dirs that are no longer public (or invalid)."""
    if not OUT_DIR.is_dir():
        return
    for child in OUT_DIR.iterdir():
        if not child.is_dir():
            continue
        if child.name in keep:
            continue
        index = child / "index.html"
        if index.exists():
            index.unlink()
        # remove empty md twin if any
        md = child / "index.html.md"
        if md.exists():
            md.unlink()
        try:
            child.rmdir()
            print("track: removed", child.relative_to(ROOT))
        except OSError:
            print("track: left non-empty", child.relative_to(ROOT))


def main() -> None:
    # Never create /proje/index.html listing.
    keep: set[str] = set()
    for item in _load_items():
        slug = build_one(item)
        if slug:
            keep.add(slug)
    sync_orphan_dirs(keep)
    print(f"track: published {len(keep)} page(s)")


if __name__ == "__main__":
    main()
