# Stage 10 — Final repository hardening & release gate

- **Branch:** `seo-rebuild`
- **HEAD:** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2` (Stages 4–10 uncommitted)
- **Working tree:** dirty (implementation + generated public HTML/md; no commit)
- **BEFORE artifacts:** frozen (`summary.json` sha256 `71f9c77685878d873be07f06610aada4912b9eac79e086a753cf59b9ec711364`)
- **Benchmark files:** `geo-queries.json`, `geo-rubric.md`, `urls.txt` checksums unchanged
- **KPI:** finding → measure → BEFORE → impl → AFTER

No commit/push. Rubric and BEFORE not modified.

---

## Repository state

| Item | Value |
|---|---|
| Branch | `seo-rebuild` (tracks `origin/seo-rebuild`) |
| HEAD | `eec81da` |
| Dirty | Yes — Stages 4–10 |
| Frozen BEFORE GEO | **2.333 / 5**, 26 failing checks |
| Stage 5 AFTER (historical) | GEO **2.956 / 5**, 10 failing checks |
| Stage 9 AFTER | GEO **3.133 / 5**, 4 failing checks |
| Stage 10 AFTER | GEO **3.133 / 5**, 4 failing checks, 39 pass, 2 unscored |

---

## Test results

| Command | Result |
|---|---|
| `python3 scripts/seo/test_schema.py` | `schema self-check ok` |
| `python3 scripts/seo/test_collect.py` | `seo collector self-check ok` |
| `python3 scripts/test_project_tracking.py` | `PASS (5 suites)` |

Re-run after the sitemap-order fix: same three commands, all pass.

---

## Build results

Documented pipeline (`README.md` / `netlify.toml` / `DEPLOY-CLOUDFLARE.md`):

```
python3 scripts/optimize_uploads.py
python3 scripts/build_production.py
python3 scripts/build_project_tracking.py
python3 scripts/scrub_customer_copy.py
python3 scripts/prerender.py
python3 scripts/build_llms.py
python3 scripts/minify_assets.py
```

(`pip install -r requirements.txt` skipped locally; deps already present.)

| Step | Result |
|---|---|
| optimize_uploads | Idempotent: 6 JPEGs kept, WebP siblings present, 0% size change |
| production + prerender + llms | Success. Sitemap 37. `build_home_a3` footer-columns warn is **EXPECTED_STATE** (Stage 6) |
| First vs second consecutive rebuild (pre-fix) | `index.html` and inner HTML identical; **sitemap.xml hash differed** (homepage `lastmod` 2026-08-30 → 2026-08-31 because sitemap ran before A3 rewrote `index.html`) |
| Fix | `merge_sitemap()` now runs **after** A3 homepage write |
| Two consecutive rebuilds after fix | **STABLE** (index.html, sitemap, llms, sampled inner pages) |
| minify_assets | Deterministic on second pass. In-place; git sources restored (`assets/*.css`, `theme.js` remain readable). Deploy-only minify, as designed |

Collector AFTER recapture:

```
AFTER captured SHA=eec81da urls=35 geo_mean=3.133 fails=4
```

Validation: `all_urls_tested`, 35 URL artifacts, JSON-LD parse completed, rubric applied to 5 URLs.

---

## SEO/GEO integrity

### Metadata (35 corpus URLs)

- Title, description, self-canonical (absolute HTTPS): **35/35**
- Duplicate titles/descriptions: **none**
- OG title/description/image/alt: **35/35**
- Twitter card: **35/35**
- Public corpus: none are `noindex`
- Homepage has no explicit `robots` meta (default index). Inner pages: `index, follow`. Not contradictory.

### Schema

- Homepage: one `<script type="application/ld+json" id="ld-json">`. Types: LocalBusiness+ProfessionalService, WebSite, WebPage, FAQPage. `data-prerendered` present. Geo, hours, logo, Instagram `sameAs`, `hasMap` (coordinate search).
- FAQPage **5** entities ↔ **5** visible `<details>` (questions match).
- Inner `#business` `@id` refs without inlining NAP: **intentional** (entity defined on homepage). Inner pages ship their own `WebSite` node, so `#website` is not dangling.
- Guide example `/bilgi/tabela-cesitleri/`: Article + BreadcrumbList + WebPage.
- JSON-LD parse: **all 35 OK**. No second LocalBusiness graph on inner pages.

### Crawl / sitemap / routes

- Sitemap: **37** unique HTTPS locs, all `lastmod` 2026-08-31, no `/admin/`, `/proje/`, `404`, or `.md`
- Corpus 35 + `/gizlilik/` + `/hakkimizda/`
- Broken internal: **0**
- Unreachable from home (corpus): **[]**
- Gone/410 links in corpus: **0**
- Placeholder slugs (`liman-kahve`, etc.) not linked from public HTML
- `/404.html`: `noindex, follow` + `_headers` `X-Robots-Tag: noindex`
- `/gizlilik/`, `/hakkimizda/`: `index, follow`, in sitemap
- `/kvkk/` → `/gizlilik/` 301 in `_redirects`
- `/admin/`, `/proje/`: git robots Disallow + `X-Robots-Tag: noindex` (`/proje/` also nofollow)
- Tracking `/proje/*/index.html`: meta noindex
- Live probes: apex 200; `/hizmetler/tabela` 301 → trailing slash; `www` 301 → apex; `/iletisim/` **404** (SEO-003: contact canonical is `/bolgeler/tekirdag/`, unchanged)

### Entity / NAP

Consistent across `content.json`, homepage JSON-LD, `llms.txt`, homepage twin İletişim stanza, Tekirdağ page, `lib_site` constants:

| Fact | Value |
|---|---|
| Name | Malt Studio |
| Domain | https://maltstudio.co |
| Email | merhaba@maltstudio.co |
| Phone | 05525826959 = +90 552 582 69 59 = tel:+905525826959 |
| Address | Yavuz Mahallesi, Ruşen Güneş Sokak, D Blok No:2, 59100 Süleymanpaşa / Tekirdağ |
| Geo | 40.9769375, 27.5041875 |
| Hours | Pazartesi–Cumartesi 09:00–19:00 |
| Instagram | https://www.instagram.com/maltstudio.co/ |
| LinkedIn | empty (Jakarta slug absent) |
| Logo | CMS empty → schema `https://maltstudio.co/images/icon-512.png` |
| Maps | coordinate search; not a Place ID |

Homepage footer Instagram remains `hidden` (same URL). Not a second entity.

### AI/GEO crawlability (repository)

- Git `robots.txt`: `Allow: /`; Disallow only `/admin/`, `/proje/`. **No** GPTBot/ClaudeBot/Google-Extended Disallow.
- `llms.txt` + `llms-full.txt` present. 37 Markdown twins. Twins `X-Robots-Tag: noindex`.
- JSON-LD and main copy in initial HTML (prerender).
- Live Cloudflare managed Disallow: **external** (TECHSEO-001). Git robots not changed to fight it.

---

## Performance integrity

- First homepage work `<img>`: `fetchpriority="high"`, **not** lazy. Later work images `loading="lazy"`.
- First OFİSO project photo: `fetchpriority="high"`.
- `<picture>` + WebP: homepage picture_count **6**; JPEG fallback kept.
- Font preloads: **4** (Big Shoulders + Inter, latin + latin-ext). Not an explosion.
- JS: deferred GA4, deferred `theme.js`, prerender skip for duplicate JSON-LD.
- `index.html` sha256 stable across identical rebuilds.
- No JPEG recompress this stage. No Lighthouse/Node added.

---

## Remaining four fails (unchanged classification)

| ID | Metric | Classification | Evidence this run |
|---|---|---|---|
| TECHSEO-001 | `live_robots_blocks_ai` | **EXTERNAL** | Live robots still Disallow GPTBot, ClaudeBot, Google-Extended. Git does not. |
| TECHSEO-005 | `gsc_meta` | **EXTERNAL** | CMS verification field empty. No invented token. Prerender will emit meta when a real token exists. |
| CONTENT-001 | `project_wordcount_min` 123 | **INTENTIONAL** | CMS project fields still empty. 123–129 words. |
| GEO-002 | `md_twin_ratio_home` 0.543 | **INTENTIONAL** | md=336 / html=619. Curated twin + `llms.txt`. Not padded to 0.70. |

Collector detail `empty expected BEFORE` on GSC is a leftover phrase in the check row, not a criterion change.

Unscored: `gbp_place_id`, LinkedIn entity scrape.

---

## Regression check (Stage 9 → Stage 10)

| | |
|---|---|
| GEO mean | Unchanged **3.133** |
| Fails | Same four |
| Per-URL GEO | Unchanged (home 3.222, tabela 3.000, tabela-cesitleri 3.778, tekirdag 3.111, ofiso 2.556) |
| Improvements | AFTER `report.md` titled as AFTER (was hardcoded “BEFORE baseline”). Stale `collector-snapshot.md` (mean 2.956 leftover) deleted. Sitemap generated after A3 so lastmod matches the rewritten homepage. |
| Regenerated | Public HTML/md from the documented pipeline (content hashes of pages stable after the lastmod catch-up). `llms-full.txt` 176147 → 175744 bytes from full twin rebuild; homepage twin still 336 words. |
| New warnings | None material. `build_home_a3` footer warn unchanged. |
| Test failures | None |

Vs frozen BEFORE: GEO 2.333 → 3.133; fails 26 → 4.

Vs Stage 5 AFTER (2.956 / 10 fails): Stage 7 closed CONTENT-003; Stages 8–9 left the remaining four as external/intentional.

---

## Repository complete

Deterministic tests pass. Rebuild is stable. Schema, metadata, crawl graph, entity NAP, AI files, and image priority are sound. The four collector fails are not repository defects.

## External actions required

Do not attempt these from git:

1. **Cloudflare AI Crawl Control** — Allow GPTBot, ClaudeBot, Google-Extended; stop managed `Disallow: /` prepend. Then re-fetch live `robots.txt`.
2. **Google Search Console** — paste a real token into CMS `googleSearchConsoleVerification`, rebuild, deploy.
3. **Google Business Profile** — create/verify off-site; then optionally replace `googleMapsUrl` with a Place URL. Repo has NAP/geo only.
4. **LinkedIn** — only a verified Malt Studio Tekirdağ company URL; never `linkedin.com/company/malt-studio`.
5. **Project/case-study copy** — only when real client/date/description exists in CMS.
6. **SERP / AI citation measurement** — after the next production deploy; not fabricated here.

---

## Final decision

STAGE 10 COMPLETE — REPOSITORY RELEASE GATE PASSED

GEO BASELINE: 2.333 / 5
CURRENT GEO: 3.133 / 5
DETERMINISTIC FAILS: 4
REMAINING FAILS: EXTERNAL/INTENTIONAL ONLY
