#!/usr/bin/env python3
"""Archive maltstudio.co URLs on the Internet Archive Wayback Machine.

Uses the public Save Page Now endpoint (no API key):
  GET https://web.archive.org/save/{url}

On success SPN responds with HTTP 302 and a Location like:
  https://web.archive.org/web/{timestamp}/{original_url}

Usage:
  python3 scripts/wayback_archive.py
  python3 scripts/wayback_archive.py --delay 8 --timeout 180
  python3 scripts/wayback_archive.py --urls-only   # print URL list, no saves

Optional auth (faster / higher limits) via archive.org S3 keys:
  export IA_ACCESS_KEY=...
  export IA_SECRET_KEY=...
  # then the script POSTs to https://web.archive.org/save with Authorization: LOW ...

Re-save later: run this script again, or open
  https://web.archive.org/save/https://maltstudio.co/
in a browser.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITEMAP = "https://maltstudio.co/sitemap.xml"
LOCAL_SITEMAP = ROOT / "sitemap.xml"
UA = "Mozilla/5.0 (compatible; MaltStudio-Archive/1.0; +https://maltstudio.co/)"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# Notable assets so OG / logo / portfolio visuals exist in Wayback even if
# outlink capture misses them.
EXTRA_ASSETS = [
    "https://maltstudio.co/images/og.jpg",
    "https://maltstudio.co/images/logo.svg",
    "https://maltstudio.co/images/icon-192.png",
    "https://maltstudio.co/images/icon-512.png",
    "https://maltstudio.co/images/uploads/6c209abf-2af4-4517-a385-92dd52cc044f.jpg",
    "https://maltstudio.co/images/uploads/img_6432.jpg",
    "https://maltstudio.co/images/uploads/img_7536.jpg",
    "https://maltstudio.co/images/uploads/img_7847.jpg",
    "https://maltstudio.co/images/uploads/49def14c-ef5f-4f6c-ba65-60a6654072b7-1-.jpg",
    "https://maltstudio.co/images/uploads/snapinsta.to_721735614_18085976048381838_6119022146079124288_n.jpg",
]


def fetch_text(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def parse_sitemap_locs(xml_text: str) -> list[str]:
    root = ET.fromstring(xml_text)
    locs = [el.text.strip() for el in root.findall("sm:url/sm:loc", NS) if el.text]
    if not locs:
        locs = [el.text.strip() for el in root.findall("url/loc") if el.text]
    return locs


def load_urls() -> list[str]:
    urls: list[str] = []
    try:
        urls.extend(parse_sitemap_locs(fetch_text(DEFAULT_SITEMAP)))
    except Exception as exc:  # noqa: BLE001
        print(f"warn: live sitemap failed ({exc}); using local {LOCAL_SITEMAP}", file=sys.stderr)
        urls.extend(parse_sitemap_locs(LOCAL_SITEMAP.read_text(encoding="utf-8")))
    urls.extend(EXTRA_ASSETS)
    seen: set[str] = set()
    out: list[str] = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


_WB_RE = re.compile(r"https?://web\.archive\.org/web/\d{10,14}/.+")


def _extract_wayback_url(*candidates: str) -> str | None:
    for c in candidates:
        if not c:
            continue
        m = _WB_RE.search(c)
        if m:
            return m.group(0).rstrip("\"')>")
    return None


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


def save_via_get(url: str, timeout: int) -> dict:
    """Public SPN: GET /save/{url} → 302 Location with Wayback snapshot.

    urllib follows redirects by default, so we disable that and read Location.
    If a follow still happens (or SPN returns 200 on the snapshot), we also
    accept a final URL matching /web/{timestamp}/...
    """
    save_url = "https://web.archive.org/save/" + url
    req = urllib.request.Request(
        save_url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        },
        method="GET",
    )
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=timeout) as resp:
            final = resp.geturl()
            body = resp.read().decode("utf-8", "replace")[:4000]
            wb = _extract_wayback_url(final, body)
            if wb:
                return {
                    "ok": True,
                    "status": resp.status,
                    "wayback_url": wb,
                    "method": "GET /save/",
                }
            return {
                "ok": False,
                "status": resp.status,
                "error": f"no wayback URL in response (status {resp.status})",
                "final_url": final,
                "method": "GET /save/",
            }
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Location") or e.headers.get("location") or ""
        if loc.startswith("/"):
            loc = "https://web.archive.org" + loc
        wb = _extract_wayback_url(loc)
        if e.code in (301, 302, 303, 307, 308) and wb:
            return {
                "ok": True,
                "status": e.code,
                "wayback_url": wb,
                "method": "GET /save/",
            }
        # Sometimes SPN returns an error page with a useful body.
        err_body = e.read().decode("utf-8", "replace")[:800]
        wb = _extract_wayback_url(err_body, loc)
        if wb:
            return {
                "ok": True,
                "status": e.code,
                "wayback_url": wb,
                "method": "GET /save/",
            }
        return {
            "ok": False,
            "status": e.code,
            "error": err_body or e.reason,
            "method": "GET /save/",
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc), "method": "GET /save/"}


def save_via_spn2_post(url: str, access: str, secret: str, timeout: int) -> dict:
    """Authenticated SPN2 POST (optional). Polls job status until done."""
    data = urllib.parse.urlencode({"url": url, "capture_all": "1"}).encode()
    req = urllib.request.Request(
        "https://web.archive.org/save",
        data=data,
        headers={
            "User-Agent": UA,
            "Accept": "application/json",
            "Authorization": f"LOW {access}:{secret}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return {
            "ok": False,
            "status": e.code,
            "error": e.read().decode("utf-8", "replace")[:500],
            "method": "SPN2 POST",
        }
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc), "method": "SPN2 POST"}

    job_id = payload.get("job_id")
    if not job_id:
        return {"ok": False, "error": f"no job_id: {payload}", "method": "SPN2 POST"}

    # Poll status
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(3)
        st_req = urllib.request.Request(
            f"https://web.archive.org/save/status/{job_id}",
            headers={
                "User-Agent": UA,
                "Accept": "application/json",
                "Authorization": f"LOW {access}:{secret}",
            },
        )
        try:
            with urllib.request.urlopen(st_req, timeout=60) as resp:
                st = json.loads(resp.read().decode("utf-8", "replace"))
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "error": f"status poll failed: {exc}", "job_id": job_id}

        status = st.get("status")
        if status == "success":
            ts = st.get("timestamp")
            orig = st.get("original_url") or url
            wb = f"https://web.archive.org/web/{ts}/{orig}" if ts else None
            return {
                "ok": True,
                "wayback_url": wb,
                "job_id": job_id,
                "timestamp": ts,
                "method": "SPN2 POST",
            }
        if status == "error":
            return {
                "ok": False,
                "error": st.get("message") or st,
                "job_id": job_id,
                "method": "SPN2 POST",
            }
    return {"ok": False, "error": "status poll timeout", "job_id": job_id, "method": "SPN2 POST"}


def save_url(url: str, timeout: int, access: str | None, secret: str | None) -> dict:
    if access and secret:
        result = save_via_spn2_post(url, access, secret, timeout)
        if result.get("ok"):
            return result
        # fall back to public GET once
        fallback = save_via_get(url, timeout)
        fallback["fallback_from"] = result
        return fallback
    return save_via_get(url, timeout)


def main() -> int:
    ap = argparse.ArgumentParser(description="Archive maltstudio.co on Wayback Machine")
    ap.add_argument("--delay", type=float, default=6.0, help="Seconds between saves (default 6)")
    ap.add_argument("--timeout", type=int, default=180, help="Per-URL timeout seconds")
    ap.add_argument("--urls-only", action="store_true", help="Print URL list and exit")
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "scripts" / "wayback_archive_results.json",
        help="Results JSON path",
    )
    args = ap.parse_args()

    urls = load_urls()
    if args.urls_only:
        for u in urls:
            print(u)
        print(f"# {len(urls)} URLs", file=sys.stderr)
        return 0

    access = os.environ.get("IA_ACCESS_KEY") or os.environ.get("SPN2_ACCESS_KEY")
    secret = os.environ.get("IA_SECRET_KEY") or os.environ.get("SPN2_SECRET_KEY")

    results: list[dict] = []
    ok_n = fail_n = 0
    started = datetime.now(timezone.utc).isoformat()
    print(f"Archiving {len(urls)} URLs (delay={args.delay}s, timeout={args.timeout}s)", flush=True)
    if access and secret:
        print("Using authenticated SPN2 POST", flush=True)
    else:
        print("Using public GET https://web.archive.org/save/{url}", flush=True)

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] save {url} ...", flush=True)
        result = save_url(url, args.timeout, access, secret)
        if not result.get("ok"):
            print(f"  retry once after failure: {result.get('error') or result}", flush=True)
            time.sleep(min(args.delay * 2, 20))
            result = save_url(url, args.timeout, access, secret)

        entry = {"url": url, **result, "at": datetime.now(timezone.utc).isoformat()}
        results.append(entry)
        if result.get("ok"):
            ok_n += 1
            print(f"  OK {result.get('wayback_url')}", flush=True)
        else:
            fail_n += 1
            print(f"  FAIL {result.get('error') or result}", flush=True)

        # Persist incrementally so a long run can be inspected mid-flight.
        payload = {
            "started": started,
            "updated": datetime.now(timezone.utc).isoformat(),
            "ok": ok_n,
            "fail": fail_n,
            "results": results,
        }
        args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        if i < len(urls):
            time.sleep(args.delay)

    print(f"\nDone. ok={ok_n} fail={fail_n} → {args.out}", flush=True)
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
