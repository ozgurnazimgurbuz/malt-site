# Stage 8 — Technical SEO, crawlability & performance

- **Branch:** `seo-rebuild`
- **HEAD:** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2` (Stages 4–8 still uncommitted)
- **BEFORE artifacts:** frozen (`summary.json` sha256 `71f9c776…11364`)
- **KPI:** finding → measure → BEFORE → impl → AFTER.

Stage 7 AFTER: GEO mean **3.133**, **4** failing checks.

Stage 8 AFTER: GEO mean **3.133**, **4** failing checks (same four, left untouched).

No commit/push.

---

## Audit (no change needed)

| Area | Result |
|---|---|
| Public sitemap | 37 unique absolute HTTPS URLs, trailing slashes, no admin/proje/404/md |
| Canonicals | Self-canonical on public HTML |
| robots.txt (git) | `Allow: /`; `Disallow: /admin/`, `/proje/`; sitemap declared |
| Live CF robots | Still Disallow AI crawlers — EXTERNAL, not git |
| Crawl graph | 0 orphans, 0 broken internals, 0 gone links in corpus |
| hizmet-bolge HTML | Not generated; 301s already in `_redirects` |
| 410 placeholders | No public HTML links to them |
| `/proje/` | meta `noindex,nofollow` + git Disallow |
| JSON-LD | Homepage LocalBusiness only; inner `#business` refs are intentional |
| Picture/WebP | Present; JPEG fallback kept |
| width/height 800×1000 | Matches 4:5 CSS tiles (`object-fit: cover`); file pixels are taller — do not retag to file size |
| CSP | Not added — would risk Decap (`unpkg`), GA4, theme JS |
| GSC / GBP / LinkedIn | Not in repo |
| Four remaining collector fails | Untouched |

---

## Fixes

### LCP image hints

- First homepage work image and first project photo: `fetchpriority="high"`, not lazy, not `decoding="async"`.
- Later images stay lazy + async.

### Headers (`_headers` + `netlify.toml`)

- `/proje/*` → `X-Robots-Tag: noindex, nofollow` (matches meta + robots)
- `/*.md` twins → `X-Robots-Tag: noindex` (AI twins, not Google duplicates)
- `/404.html` → `X-Robots-Tag: noindex`
- `/assets/*.js` week-long cache (CSS already had this)
- `Strict-Transport-Security: max-age=31536000` (no `includeSubDomains`)

### Build determinism

- `build_home_a3.inject_css` accumulated blank lines on every rebuild.
- Strip now eats prior A3 block + leftover whitespace. Identical rebuilds: `index.html` hash stable.

### robots.txt

- Comment only: live Cloudflare Managed Content may differ from this file.

---

## Not done (on purpose)

- No JPEG recompress (quality).
- No CSP.
- No www→apex redirect invented without host-rule evidence.
- `minify_assets.py` still in-place on Netlify publish; not run locally (would dirty git CSS).
- Sitemap `lastmod` is HTML mtime after rewrite (same calendar day for a full rebuild). Honest enough; git-blame lastmod not added.

---

## Tests

```
python3 scripts/seo/test_schema.py          # ok
python3 scripts/seo/test_collect.py        # ok
python3 scripts/test_project_tracking.py  # PASS (5 suites)
python3 scripts/seo/collect.py --out artifacts/geo-seo/after --phase AFTER
```

Identical production+prerender+llms rebuild: `index.html` stable.
BEFORE checksum unchanged.
GEO mean still **3.133**. Fails still TECHSEO-001, TECHSEO-005, CONTENT-001, GEO-002.
