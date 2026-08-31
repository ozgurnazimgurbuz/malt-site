# Stage 12 — Commit, push & production activation

- **Branch:** `seo-rebuild`
- **Rebuild commit SHA:** `c3335d831ca9e67ea9d0a2149424a545921968f1`
- **Parent:** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2`
- **Remote:** `origin` → `https://github.com/ozgurnazimgurbuz/malt-site.git`
- **Push:** `seo-rebuild` → `origin/seo-rebuild` verified (`git ls-remote` = `c3335d8`)
- **`origin/main`:** still `eec81da4a47dc77005eb64bab3cb2c63c931a3c2` (not updated)
- **BEFORE frozen:** `artifacts/geo-seo/before/summary.json` sha256 `71f9c77685878d873be07f06610aada4912b9eac79e086a753cf59b9ec711364`
- **Rubric / queries:** not modified
- **`before/` / `after/`:** not overwritten this stage

No merge to `main`. No fabricated GSC / GBP / LinkedIn / rankings / AI-citation / Lighthouse data.

---

## Pre-commit

| Check | Result |
|---|---|
| Branch | `seo-rebuild` tracking `origin/seo-rebuild` |
| Tests | `test_schema.py` ok · `test_collect.py` ok · `test_project_tracking.py` PASS (5 suites) |
| Production build | success (local minify skipped; deploy pipeline still minifies) |
| Collector AFTER (local tree) | `geo_mean=3.133` `fails=4` |

Four known failures unchanged:

| ID | Classification |
|---|---|
| TECHSEO-001 | EXTERNAL — live Cloudflare managed `Disallow: /` for GPTBot, ClaudeBot, Google-Extended |
| TECHSEO-005 | EXTERNAL — empty GSC token in `content.json` |
| CONTENT-001 | INTENTIONAL — sparse CMS project records |
| GEO-002 | INTENTIONAL — homepage `.html.md` twin ratio 0.543 |

No new regression. Stages 4–10 production files are in the rebuild commit. Stage 11 `artifacts/geo-seo/live/` remains a separate directory.

---

## Commit & push

- One rebuild commit: `feat(seo): complete GEO and technical SEO rebuild` (`c3335d8`)
- Push: **`seo-rebuild` → `origin/seo-rebuild` only** (`eec81da..c3335d8`)
- **Not** pushed to `main`
- **Not** merged

This report file was updated after that push so the SHA and remote verification could be recorded. It does not change production HTML.

---

## Production path

Documented (`DEPLOY-CLOUDFLARE.md`, README): **`main` → Cloudflare Pages → maltstudio.co**.

There is no GitHub Actions workflow. `wrangler` is not installed. No Pages production-branch override was used.

Pushing `seo-rebuild` therefore does **not** deploy production. A PR/merge into `main` is required.

Live response headers on 2026-08-31 still include `cache-status: "Netlify Edge"` and `x-nf-request-id`, with `server: cloudflare`. That is consistent with Cloudflare in front of an origin that has not received `c3335d8`. It does not change the rule: do not treat `seo-rebuild` as production.

**Production deployment status:** pending.

---

## Live HTTP (current public origin — still pre-rebuild)

Independent curl against `https://maltstudio.co` after the push. This is **not** validation of `c3335d8`; it proves production is still the old tree.

| URL | Status | Notes |
|---|---|---|
| `/` | 200 | Thin prerendered JSON-LD only |
| `/hizmetler/tabela/` | 200 | |
| `/bilgi/tabela-cesitleri/` | 200 | no Article JSON-LD in static HTML |
| `/bolgeler/tekirdag/` | 200 | |
| `/projeler/ofiso/` | 200 | |
| `/hakkimizda/` | **404** | new route not live |
| `/gizlilik/` | **404** | new route not live |
| `/kvkk/` | **404** | no 301 → `/gizlilik/` |
| `/404.html` | 404 | Netlify default 404 path; rebuild noindex not live |
| `/robots.txt` | 200 | Cloudflare Managed Content prepends AI Disallow |
| `/sitemap.xml` | 200 | |
| `/llms.txt` | 200 | |
| `/llms-full.txt` | 200 | |
| `/index.html.md` | 200 | |
| `/hizmetler/tabela/index.html.md` | 200 | |
| `/bilgi/tabela-cesitleri/index.html.md` | 200 | |

`/kvkk/` followed with `-L` stayed 404 (no redirect hop).

---

## Live schema / metadata (no JavaScript)

Homepage static `<script type="application/ld+json" id="ld-json">` is a single `@graph` node:

- `@id` `#business` — LocalBusiness + ProfessionalService
- NAP + Instagram `sameAs` only
- **Missing in prerendered JSON-LD:** `#website`, `#webpage`, `geo`, `openingHoursSpecification`, `logo`, `image`, `knowsAbout`, `hasMap`, `FAQPage`

`#website` / `#webpage` strings exist only inside a client-side script that injects JSON-LD after JS runs. Stage 12 live check is without JS, so they do **not** count.

Guide `/bilgi/tabela-cesitleri/`: no Article schema in static HTML.

Homepage metadata that **is** present on the old origin: canonical `https://maltstudio.co/`, `og:title` / `og:url` / `og:image`, `twitter:card`.

---

## Live robots

`https://maltstudio.co/robots.txt` still prepends:

```
# BEGIN Cloudflare Managed content
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /
```

**TECHSEO-001** remains **EXTERNAL — ACTION REQUIRED**. Repository `robots.txt` was not changed to compensate.

---

## Old-live problems vs this push

Stage 11 old-live snapshot problems are **not** resolved on the public origin, because `c3335d8` is not on `main` / not deployed:

| Old-live issue | Live after Stage 12 push |
|---|---|
| Homepage thin JSON-LD | still thin |
| Missing Website/WebPage in static HTML | still missing |
| Missing geo / hours / logo / knowsAbout / hasMap | still missing in prerendered LD |
| Missing FAQPage | still missing |
| Missing guide Article schema | still missing |
| Missing `/hakkimizda/` | still 404 |
| Missing `/gizlilik/` | still 404 |
| Missing `/kvkk/` → `/gizlilik/` | still 404 |

Do not claim these fixed until live HTML after a `main` deploy proves it.

Collector was **not** re-run into `artifacts/geo-seo/live/` this stage (would overwrite the Stage 11 old-live snapshot without a new deploy).

### BEFORE → AFTER → LIVE

| Phase | GEO mean | Deterministic fails | Notes |
|---|---|---|---|
| BEFORE | 2.333 / 5 | 26 | frozen `eec81da` |
| AFTER | 3.133 / 5 | 4 | local / committed tree |
| LIVE | Stage 11 snapshot | old origin | production still `eec81da` |

---

## Remaining external actions

1. **PR / merge `seo-rebuild` → `main`**, then confirm Cloudflare (or current origin) production deploy of `c3335d8`
2. Cloudflare AI Crawl Control — Allow GPTBot / ClaudeBot / Google-Extended; stop managed `Disallow: /` prepend
3. Real GSC verification token (`googleSearchConsoleVerification`)
4. Real GBP / Place ID
5. Real Tekirdağ LinkedIn company URL (never Jakarta `linkedin.com/company/malt-studio`)
6. Rankings / AI Overviews / ChatGPT / Perplexity / Gemini citations / Lighthouse — **not measured, not claimed**

---

## Regressions

None in the committed tree (tests + AFTER collector). Live origin is unchanged, not a new regression.

---

STAGE 12 COMPLETE — REPOSITORY COMMITTED & PUSHED — PRODUCTION DEPLOYMENT PENDING
