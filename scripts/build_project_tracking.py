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


class TrackValidationError(ValueError):
    """CMS data conflict — fail the build instead of guessing."""


def _format_tr_date(raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        return ""
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
            print(f"track: skip {path.name}: {exc}", file=sys.stderr)
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


def validate_and_resolve(
    steps: list[dict],
    current_step: int | None,
    *,
    source: str = "proje",
) -> tuple[list[dict], int]:
    """Resolve current step; raise on currentStep vs status conflict.

    Rules:
    - >1 status=current → error
    - 1 status=current and currentStep set to a different index → error
    - 0 status=current and currentStep in range → derive statuses from currentStep
    - 0 status=current and no currentStep → error
    """
    if not steps:
        raise TrackValidationError(f"{source}: en az bir aşama gerekli")

    currents = [i for i, s in enumerate(steps) if s["status"] == "current"]
    if len(currents) > 1:
        nums = ", ".join(str(i + 1) for i in currents)
        raise TrackValidationError(
            f"{source}: birden fazla aşamada status=current ({nums}). "
            "Yalnızca bir aşama 'Şu an' olmalı."
        )

    if len(currents) == 1:
        idx = currents[0]
        if current_step is not None and current_step != idx + 1:
            raise TrackValidationError(
                f"{source}: currentStep={current_step} ama steps[{idx + 1}] "
                f"('{steps[idx]['title']}') status=current. "
                "currentStep ile steps[].status çelişiyor — birini düzeltin."
            )
        return steps, idx + 1

    if current_step is None:
        raise TrackValidationError(
            f"{source}: hiçbir aşamada status=current yok ve currentStep boş. "
            "Bir aşamayı 'Şu an' yapın veya currentStep girin."
        )
    if not (1 <= current_step <= len(steps)):
        raise TrackValidationError(
            f"{source}: currentStep={current_step} geçersiz "
            f"(1–{len(steps)} arası olmalı)."
        )

    idx = current_step - 1
    for i, s in enumerate(steps):
        if i < idx:
            s["status"] = "completed"
        elif i == idx:
            s["status"] = "current"
        else:
            s["status"] = "pending"
    return steps, current_step


def _timeline_html(steps: list[dict]) -> str:
    items = []
    for s in steps:
        st = s["status"]
        mark = {"completed": "✓", "current": "●", "pending": "○"}[st]
        label = {"completed": "Tamamlandı", "current": "Şu an", "pending": "Bekliyor"}[st]
        # completedDate only on completed steps (never invent for current/pending).
        if st == "completed" and s["completedDate"]:
            done_disp = _format_tr_date(s["completedDate"])
            dt = html.escape(s["completedDate"][:10])
            label_html = (
                f'<div class="track-step-status">{label} · '
                f'<time datetime="{dt}">{html.escape(done_disp)}</time></div>'
            )
        else:
            label_html = f'<div class="track-step-status">{label}</div>'
        desc = (
            f'<p class="track-step-desc">{html.escape(s["description"])}</p>'
            if s["description"]
            else ""
        )
        items.append(
            f'<li class="track-step track-step--{st}" data-status="{st}">'
            f'<span class="track-mark" aria-hidden="true">{mark}</span>'
            f'<div class="track-step-body">'
            f'<div class="track-step-title">{html.escape(s["title"])}</div>'
            f"{label_html}{desc}"
            f"</div></li>"
        )
    return f'<ol class="track-timeline">{"".join(items)}</ol>'


def build_one(item: dict) -> str | None:
    """Write one page; return slug if written. Raises TrackValidationError on bad data."""
    source = str(item.get("_source") or item.get("slug") or "proje")
    slug = str(item.get("slug") or "").strip().strip("/")
    if not slug or not SLUG_RE.fullmatch(slug):
        raise TrackValidationError(
            f"{source}: geçersiz slug {slug!r} "
            "(yalnızca küçük harf, rakam, tire; örn. mantar-garage-7f3k9x)"
        )
    if not item.get("public", True):
        return None

    project = str(item.get("projectName") or "").strip()
    client = str(item.get("clientName") or "").strip()
    if not project or not client:
        raise TrackValidationError(f"{source}: projectName ve clientName zorunlu")

    steps = _normalize_steps(item.get("steps"))
    if not steps:
        raise TrackValidationError(f"{source}: en az bir aşama gerekli")

    raw_cs = item.get("currentStep")
    try:
        cs = int(raw_cs) if raw_cs not in (None, "") else None
    except (TypeError, ValueError) as exc:
        raise TrackValidationError(f"{source}: currentStep sayı olmalı") from exc

    steps, current_n = validate_and_resolve(steps, cs, source=source)
    current = steps[current_n - 1] if current_n else {}
    current_title = str(current.get("title") or "")
    current_desc = str(current.get("description") or "").strip()

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

    current_desc_html = (
        f'<p class="track-now-desc">{html.escape(current_desc)}</p>'
        if current_desc
        else ""
    )

    last_html = ""
    if last_disp:
        dt = html.escape(last_raw[:10] if last_raw else "")
        last_html = (
            f'<div class="track-updated">'
            f'<div class="track-updated-label">Son güncelleme</div>'
            f'<time datetime="{dt}">{html.escape(last_disp)}</time>'
            f"</div>"
        )

    wa_msg = f"Merhaba, {client} / {project} projesi hakkında sorum var."
    # Hierarchy: client → project → ŞU ANDA → title → desc → lastUpdated → timeline → CTA
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
    <div class="track-now" role="status">
      <div class="track-now-label">Şu anda</div>
      <p class="track-now-name">{html.escape(current_title)}</p>
      {current_desc_html}
      {last_html}
    </div>
  </div>
</section>
<section class="page-main track-main">
  <div class="wrap track-wrap">
    <h2 class="track-status-heading">Proje durumu</h2>
    {_timeline_html(steps)}
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
    # Cache-bust track CSS without rebuilding every public page.
    page = page.replace("site.css?v=theme2", "site.css?v=track3")
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
    errors: list[str] = []
    for item in _load_items():
        try:
            slug = build_one(item)
        except TrackValidationError as exc:
            errors.append(str(exc))
            continue
        if slug:
            keep.add(slug)
    sync_orphan_dirs(keep)
    print(f"track: published {len(keep)} page(s)")
    if errors:
        for e in errors:
            print(f"track ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
