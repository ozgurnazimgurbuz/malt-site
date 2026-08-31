# Stage 11 — Deployment & external SEO/GEO activation

- **Branch:** `seo-rebuild`
- **HEAD / origin:** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2`
- **Working tree:** dirty (Stages 4–10 uncommitted; not discarded)
- **BEFORE:** frozen (`71f9c776…11364`)
- **Rubric / queries:** not edited
- **No commit. No push.**

---

## Pre-deploy gate

| Check | Result |
|---|---|
| `python3 scripts/seo/test_schema.py` | ok |
| `python3 scripts/seo/test_collect.py` | ok |
| `python3 scripts/test_project_tracking.py` | PASS (5 suites) |
| Production build (`optimize` skipped this pass; `build_production` → tracking → scrub → prerender → llms) | success, sitemap 37 |
| Collector AFTER | `geo_mean=3.133` `fails=4` |

A parallel collector run during rebuild briefly reported 6 fails (PERF picture/lazy mid-A3). Recapture on the finished tree: **4 fails**, same as Stage 10. Not a regression.

Known four still correctly classified:

| ID | Classification |
|---|---|
| TECHSEO-001 | EXTERNAL |
| TECHSEO-005 | EXTERNAL |
| CONTENT-001 | INTENTIONAL |
| GEO-002 | INTENTIONAL |

**Deployment candidate:** working tree on top of `eec81da`. There is no separate git SHA for Stages 4–10 because they were never committed.

---

## Deploy

**Not executed.**

Documented mechanism (`DEPLOY-CLOUDFLARE.md` / README): Cloudflare Pages production branch **`main`**, build from GitHub. `origin/main` is still `eec81da`. Wrangler is not installed.

Stage 11 critical rules forbid commit/push, so the SEO rebuild cannot reach the live origin from this session.

Live checks below are of **currently published** production, not the local Stage 10 tree.

---

## Live URL checks (`https://maltstudio.co`)

| URL | HTTP |
|---|---|
| homepage | 200 |
| `/hizmetler/tabela/` | 200 |
| `/bilgi/tabela-cesitleri/` | 200 |
| `/bolgeler/tekirdag/` | 200 |
| `/projeler/ofiso/` | 200 |
| `/hakkimizda/` | **404** |
| `/gizlilik/` | **404** |
| `/kvkk/` | **404** (expected 301 only after deploy of `_redirects`) |
| `/404.html` | **404** (host default ~3808 B; no `X-Robots-Tag`) |
| sitemap | 200 |
| robots.txt | 200 |
| llms.txt | 200 |
| llms-full.txt | 200 |
| Markdown twins (home, tabela, guide) | 200 |

---

## Live HTML / JSON-LD (before JavaScript)

Compared to local Stage 10: **expected mismatch** (rebuild not on origin). Diagnosis: live is pre–Stage 4 prerender graph.

| Signal | Local Stage 10 | Live origin |
|---|---|---|
| `#business` | yes, full | yes, NAP only |
| `#website` | yes | **no** |
| `#webpage` | yes | **no** |
| geo / hours / logo / image / knowsAbout / hasMap | yes | **no** |
| FAQPage | yes (5 FAQs) | **no** in source LD |
| `data-prerendered` | yes | yes (so JS does not upgrade schema) |
| Guide Article | yes | **no JSON-LD on live guide** |
| GSC meta | empty | empty |
| `og:image:alt` | page title | stale “Marka Stratejisi ve Yaratıcı Ajans” |

STOP condition: live ≠ local. Cause is undeployed working tree, not a silent production defect in the new code.

---

## Cloudflare AI crawlers (TECHSEO-001)

Live `robots.txt` still contains managed:

```
User-agent: GPTBot
Disallow: /
User-agent: ClaudeBot
Disallow: /
User-agent: Google-Extended
Disallow: /
```

Git `robots.txt` was not changed.

**Dashboard action (only if Özgür authorizes Cloudflare access):**

1. [dash.cloudflare.com](https://dash.cloudflare.com) → zone `maltstudio.co`
2. **AI Crawl Control** → Crawlers → **Allow** GPTBot, ClaudeBot, Google-Extended
3. Disable or retune **Bot Preference Sync / Managed robots.txt** so those three are not prepended as `Disallow: /`
4. Re-fetch `https://maltstudio.co/robots.txt` — do not treat a screenshot as proof

This session: **no dashboard change**. Finding remains unresolved.

---

## GSC (TECHSEO-005)

CMS `googleSearchConsoleVerification` is still `""`. No token was supplied. Live HTML has no `google-site-verification` meta. Unresolved.

---

## GBP (LOCAL-001)

No Place ID or owned listing was verified. CMS URL is coordinate search only. Search did not surface a distinct Malt Studio Süleymanpaşa GBP.

`LOCAL-001 — EXTERNAL ACTION REQUIRED`

---

## LinkedIn (BRAND-001)

Only company URL found: Jakarta `linkedin.com/company/malt-studio` (maltstudio.com). Personal profile is attached to that entity. **Excluded.** `sameAs` not modified.

---

## Performance

Lighthouse not installed. Browser opened the live homepage; CDP then disconnected. LCP/CLS/TBT and whether the browser transferred WebP: **NOT MEASURED**. Live homepage uncompressed HTML ≈ 77 293 bytes.

---

## Frozen GEO query observations

File: `artifacts/geo-seo/live/raw/geo-query-observations.json`

- Branded queries: maltstudio.co URLs **observed** in search snippets (rank not measured).
- `Tekirdağ tabela`: maltstudio.co **observed** among other firms.
- `ışıklı tabela nedir`: maltstudio.co **observed**, not the dominant definition result.
- Google AI Overviews, Bing, ChatGPT, Perplexity, Gemini: **unable to measure**.

---

## Repository vs live

| | GEO | Notes |
|---|---|---|
| Repository BEFORE | 2.333 / 5 | frozen |
| Repository AFTER (this tree) | **3.133 / 5** | 4 deterministic fails |
| Live origin | **not scored with the Stage 10 graph** | published HTML is the pre-rebuild schema |

---

## Finding classification

| Finding | Status |
|---|---|
| TECHSEO-001 | EXTERNAL — ACTION REQUIRED |
| TECHSEO-005 | EXTERNAL — ACTION REQUIRED |
| CONTENT-001 | INTENTIONAL |
| GEO-002 | INTENTIONAL |
| LOCAL-001 | EXTERNAL — ACTION REQUIRED |
| BRAND-001 | EXTERNAL — ACTION REQUIRED |
| EXTERNAL-001 | NOT MEASURED |
| SCHEMA-001…004, SEO-001, CONTENT-004/005, legal pages | FIXED REPO / UNVERIFIED LIVE |
| REGRESSED | none in the repository collector (3.133 / 4) |

---

## Unresolved external actions

1. Commit + push `seo-rebuild` → `main` (or Wrangler direct upload) so Stage 4–10 HTML goes live — **blocked this session by no-commit/no-push**
2. Cloudflare AI Crawl Control Allow for GPTBot / ClaudeBot / Google-Extended
3. Real GSC verification token in CMS, then rebuild + deploy
4. Real GBP, then optional Place URL in CMS
5. Real Tekirdağ LinkedIn company page (never Jakarta)
6. SERP rank / AIO / ChatGPT / Perplexity / Gemini measurement after deploy

Artifacts: `artifacts/geo-seo/live/` (summary, report, raw robots/HTML/schema/observations). BEFORE and AFTER directories were not used as the live dump.

---

STAGE 11 COMPLETE — EXTERNAL VALIDATION INCOMPLETE
