# Stage 4 implementation report

- **Date:** 2026-08-30
- **Branch:** `seo-rebuild`
- **Base SHA (BEFORE, unchanged):** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2`
- **AFTER benchmark:** not run

## Finding IDs addressed (in repo)

| ID | Change |
|---|---|
| SCHEMA-001 / SCHEMA-002 / LOCAL-002 | Homepage prerender JSON-LD: LocalBusiness+ProfessionalService `#business`, WebSite `#website`, WebPage, geo, hours, logo, image, knowsAbout, hasMap (CMS maps search URL), Instagram sameAs. JS still skipped when `data-prerendered`. |
| SCHEMA-003 | FAQPage from the same visible `<details>` pairs (home extracted from `.home-faq`; inner pages from `faq_html` lists). |
| SCHEMA-004 | `/bilgi/{slug}/` WebPage + Article + FAQPage + BreadcrumbList. Hubs: WebPage. |
| SCHEMA-004 / sectors | `/sektorler/*` WebPage + BreadcrumbList + FAQPage (not Article). |
| SEO-001 | `og:image:alt` / `twitter:image:alt` from `seoTitle` (home) and page title (inner `head()`). |
| SEO-002 | Space after H2 `<br>` on homepage sector/knowledge titles. |
| CONTENT-005 | `/gizlilik/` short notice from actual NAP + WhatsApp/email + GA4 mention. `/kvkk/` → `/gizlilik/` 301. |
| CONTENT-004 | `/hakkimizda/` from existing footer/NAP copy only. No founder, no metrics. |
| TECHSEO-002 | Sitemap `lastmod` from HTML file mtime; all locs dated. Added gizlilik + hakkimizda (37 URLs). |
| PERF-002 | First homepage work-grid image is not `loading="lazy"`. `<picture>` + WebP kept. |
| 404 | `404.html` noindex, follow; not in sitemap. |

## Intentionally not implemented as repo “fixes”

| ID | Reason |
|---|---|
| TECHSEO-001 | Cloudflare Managed robots. Git `robots.txt` already Allow `/` except `/admin/` `/proje/`. |
| BRAND-001 | CMS LinkedIn empty. Jakarta URL not added. |
| LOCAL-001 GBP | No Place ID / GBP URL in repo. `hasMap` is existing coordinate search URL only. |
| SCHEMA-005 sameAs | Empty LinkedIn/YouTube left out. |
| EXTERNAL-001 / AI citations | External. |
| CONTENT-001 | No genuine 400-word case facts. Honest “proje kaydı” blurb only. |
| PERF-001 HAR bytes | JPEGs already at card max; no quality-risk recompress. No Lighthouse. |
| TECHSEO-005 GSC | Verification field still empty. GA4 unchanged. |

## Tests

- `python3 scripts/seo/test_schema.py` — pass
- `python3 scripts/seo/test_collect.py` — pass
- `python3 scripts/test_project_tracking.py` — pass
- `python3 scripts/build_production.py && python3 scripts/prerender.py && python3 scripts/build_llms.py` — pass (`sitemap 37`)

## Limitations / notes

- `build_home_a3` logged `footer columns pattern not found; skipping footer enrich`. Homepage footer still contains Gizlilik/Hakkımızda from `index.html`.
- Shared `footer()` now links legal pages on tracking URLs too.
- Inner-page JSON-LD still references `#business` without inlining NAP (defined on homepage).
- `hasMap` is not a Google Business Profile Place URL.
