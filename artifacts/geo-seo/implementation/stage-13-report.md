# Stage 13 — Merge to main & production deployment

- **Branch after merge:** `main`
- **Merge type:** fast-forward `eec81da` → `7034fed` (no squash, no rebase, no force)
- **Rebuild commit (contained):** `c3335d831ca9e67ea9d0a2149424a545921968f1`
- **Resulting `main` SHA:** `7034fed7240c2f319305e068844b38d4ca1c60b4`
- **Push:** `main` → `origin/main` (`eec81da..7034fed`, non-fast-forward not used)
- **`origin/seo-rebuild`:** `7034fed` (unchanged; same tree)
- **BEFORE artifacts / rubric / queries:** not modified
- **No new SEO optimizations. No fabricated GSC/GBP/LinkedIn/SERP/AI-citation/Lighthouse data.**

---

## Pre-merge

| Check | Result |
|---|---|
| Current branch (start) | `seo-rebuild` @ `7034fed`, clean |
| `origin/main` | `eec81da` |
| `origin/seo-rebuild` | `7034fed` |
| Merge-base | `eec81da` |
| Commits on `seo-rebuild` not in `main` | `c3335d8` rebuild · `7034fed` Stage 12 report |
| `test_schema.py` | `schema self-check ok` |
| `test_collect.py` | `seo collector self-check ok` |
| `test_project_tracking.py` | `PASS (5 suites)` |
| Production build | `build_production` → tracking → scrub → prerender → llms; sitemap 37; working tree stayed clean |
| Collector `--out after --phase AFTER` | `geo_mean=3.133` `fails=4` |

Four known fails unchanged: TECHSEO-001, TECHSEO-005, CONTENT-001, GEO-002.

AFTER recapture timestamped `artifacts/geo-seo/after/` and was **restored** before merge so the merge did not include collector-noise diffs.

---

## Merge & push

```
git checkout main
git merge --ff-only seo-rebuild   # Updating eec81da..7034fed
git push origin main              # eec81da..7034fed  main -> main
```

`git merge-base --is-ancestor c3335d8 origin/main` → yes.

Working tree was clean after the merge. No unrelated commits.

---

## Cloudflare deployment

GitHub check **Cloudflare Pages** on `7034fed`:

- conclusion: **success**
- run: https://github.com/ozgurnazimgurbuz/malt-site/runs/99421892318
- Preview URL: `https://134055e1.malt-site.pages.dev`

That is the documented Pages build for `main`. It is **not** the same as `https://maltstudio.co`.

Public `maltstudio.co` still answers with `cache-status: "Netlify Edge"`. Polled `/hakkimizda/` and homepage `#ld-json` for 8 minutes after the push, then again after the Pages check succeeded: still old tree.

Local `curl` to `*.pages.dev` SSL-timed out; independent WebFetch of the preview host succeeded.

### Preview host (rebuild observable)

| URL | Observation |
|---|---|
| `/` | homepage + SSS/FAQ copy |
| `/hizmetler/tabela/` | 200 |
| `/bilgi/tabela-cesitleri/` | 200 guide |
| `/bolgeler/tekirdag/` | 200 |
| `/projeler/ofiso/` | 200 |
| `/hakkimizda/` | 200 Hakkımızda |
| `/gizlilik/` | 200 Gizlilik |
| `/kvkk/` | WebFetch landed on Gizlilik copy (redirect follow; 301 not measured as a status code) |
| `/404.html` | custom “Sayfa bulunamadı” |
| `/robots.txt` | git file: `Allow: /`, Disallow `/admin/` `/proje/`; **no** GPTBot Disallow |
| `/llms.txt` | includes hakkimizda + gizlilik |

Preview `robots.txt` is the git file. It does **not** prove custom-domain robots after Cloudflare AI Crawl Control.

Repo `404.html` includes `<meta name="robots" content="noindex, follow">` and `_headers` `X-Robots-Tag: noindex` on `/404.html`. Not proven on `maltstudio.co` (still generic Netlify 404).

---

## Public origin HTTP (`https://maltstudio.co`)

Captured 2026-08-31 after `origin/main` contained `7034fed`. File: `artifacts/geo-seo/live/raw/url-checks-stage13.json`.

| URL | Status | Notes |
|---|---|---|
| `/` | 200 | Netlify Edge **hit**, TTL ~1y |
| `/hizmetler/tabela/` | 200 | Edge hit |
| `/bilgi/tabela-cesitleri/` | 200 | |
| `/bolgeler/tekirdag/` | 200 | |
| `/projeler/ofiso/` | 200 | |
| `/hakkimizda/` | **404** | Edge hit |
| `/gizlilik/` | **404** | |
| `/kvkk/` | **404** | `-L` still 404; no 301 |
| `/404.html` | 404 | generic; no rebuild noindex header |
| `/robots.txt` | 200 | Cloudflare Managed AI Disallow |
| `/sitemap.xml` | 200 | |
| `/llms.txt` | 200 | |
| `/llms-full.txt` | 200 | |
| `.html.md` twins sampled | 200 | |

---

## Public origin static HTML (no JavaScript)

Homepage `#ld-json` still:

- `#business` LocalBusiness + ProfessionalService
- NAP + Instagram `sameAs` only
- **Missing:** `#website`, `#webpage`, `geo`, `openingHoursSpecification`, `logo`, `image`, `knowsAbout`, `hasMap`, `FAQPage`

Canonical / OG / Twitter on the old homepage remain present.

`/bilgi/tabela-cesitleri/`: no prerendered Article JSON-LD.

Repository `index.html` on `7034fed` **does** contain the full graph (geo, hours, logo, image, knowsAbout, hasMap, FAQPage, `#website`, `#webpage`). Public origin does not serve that file.

---

## Live robots (`maltstudio.co/robots.txt`)

Cloudflare Managed Content still:

```
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /
```

**TECHSEO-001 — EXTERNAL — ACTION REQUIRED.** Git `robots.txt` not edited.

---

## Collector

`collect.py` reads **repository** HTML and only fetches live `robots.txt`.

A run into `artifacts/geo-seo/live/` would print `geo_mean=3.133` from local files while public HTML is still the old tree. That would falsify LIVE.

**Not run** against `live/` as a production success snapshot.

Stage 11 old-live files copied to `artifacts/geo-seo/live-stage-11-old-origin/` before this stage’s new public captures.

Repository AFTER (this SHA): **3.133 / 5**, 4 fails.

---

## BEFORE → AFTER → LIVE

| Phase | GEO mean | Fails | What it measured |
|---|---|---|---|
| BEFORE | **2.333 / 5** | 26 | frozen `eec81da` |
| AFTER | **3.133 / 5** | 4 | committed tree |
| LIVE public `maltstudio.co` | **not rescored** | old origin | still thin LD, new routes 404 |
| Cloudflare Pages preview | rebuild HTML present | n/a | not the custom domain |

LIVE ≠ AFTER. Difference: custom domain still Netlify Edge (long-lived hits on `/` and `/hakkimizda/`); Pages preview is `7034fed`.

---

## Remaining external actions

1. Point `maltstudio.co` at the Cloudflare Pages production alias (or flush/remove Netlify Edge in front of the apex) so the public origin serves `7034fed`
2. Re-verify public HTTP + static JSON-LD, then run collector into `artifacts/geo-seo/live/`
3. Cloudflare AI Crawl Control — Allow GPTBot / ClaudeBot / Google-Extended
4. Real GSC verification token
5. Real GBP / Place ID
6. Real Tekirdağ LinkedIn (never Jakarta)
7. Rankings / AI Overviews / ChatGPT / Perplexity / Gemini / Lighthouse — **not measured**

---

## Regressions

None in the merged tree. Public origin mismatch is **undeployed custom domain / still-Netlify origin**, not a repository regression.

---

STAGE 13 COMPLETE — MAIN UPDATED — PRODUCTION DEPLOYMENT NOT YET VERIFIED
