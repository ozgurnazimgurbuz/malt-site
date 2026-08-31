# LIVE origin capture — 2026-08-31

Independent fetch of `https://maltstudio.co` (no JS execution). BEFORE/AFTER artifacts were not overwritten.

## Deployment

**Not performed.** Documented mechanism is Cloudflare Pages on GitHub `main`. Stage 11 forbids commit/push. `origin/main` = `origin/seo-rebuild` = `eec81da`. Stages 4–10 remain in the working tree. `wrangler` is not installed.

Live HTML matches the **currently published** origin (thin homepage JSON-LD), not the local Stage 10 working tree.

## URL checks

| URL | Status |
|---|---|
| `/` | 200 |
| `/hizmetler/tabela/` | 200 |
| `/bilgi/tabela-cesitleri/` | 200 |
| `/bolgeler/tekirdag/` | 200 |
| `/projeler/ofiso/` | 200 |
| `/hakkimizda/` | **404** (page exists only in uncommitted tree) |
| `/gizlilik/` | **404** |
| `/kvkk/` | **404** (no 301 on live; redirect is uncommitted) |
| `/404.html` | **404** (no custom file on live; 3808-byte host 404 body; no `X-Robots-Tag` observed) |
| `/sitemap.xml` | 200 (lastmod 2026-08-11; some locs undated; no gizlilik/hakkimizda) |
| `/robots.txt` | 200 |
| `/llms.txt` | 200 |
| `/llms-full.txt` | 200 |
| `/index.html.md` | 200 |
| `/hizmetler/tabela/index.html.md` | 200 |
| `/bilgi/tabela-cesitleri/index.html.md` | 200 |

## Live schema (source HTML, before JS)

Homepage prerendered JSON-LD is NAP-only:

- `#business` present (LocalBusiness + ProfessionalService)
- `#website` **absent**
- `#webpage` **absent**
- geo / hours / logo / image / knowsAbout / hasMap / FAQPage **absent**
- `data-prerendered="1"` so client JS **does not** fill the richer graph

Service `/hizmetler/tabela/`: WebPage + Service + BreadcrumbList in source (no FAQPage in this capture’s type list).

Guide `/bilgi/tabela-cesitleri/`: **no** `application/ld+json` in live HTML → Article schema not live.

OG `og:image:alt` live: `Malt Studio — Marka Stratejisi ve Yaratıcı Ajans` (stale vs local Stage 10 title-based alt).

## Live robots

Cloudflare Managed Content still `Disallow: /` for GPTBot, ClaudeBot, Google-Extended. Git `robots.txt` was not edited.

## GSC / GBP / LinkedIn

- GSC meta empty on live. CMS field empty. No token supplied.
- No verified GBP Place ID. CMS `googleMapsUrl` is coordinate search only.
- No verified Tekirdağ LinkedIn company URL. Jakarta `linkedin.com/company/malt-studio` excluded.

## Performance

Lighthouse not installed. Browser CDP disconnected after opening the homepage. LCP/CLS/TBT/WebP transfer: **not measured**. Uncompressed HTML document ≈ 77 KB on `/`.

## GEO queries

Frozen file untouched. Snippet-level observation only. Branded and some non-branded queries returned maltstudio.co URLs. Rank, AIO, Bing, ChatGPT, Perplexity, Gemini: **unable to measure**.
