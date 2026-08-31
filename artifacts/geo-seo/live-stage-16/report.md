# GEO/SEO AFTER capture

- **AFTER SHA:** `76be2139562a8965a64aa735980ca70a74693233`
- **Branch:** `main`
- **Benchmark date:** 2026-08-31T10:03:18Z
- **Python:** 3.9.6
- **Pillow:** 11.3.0
- **Chrome:** /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
- **Lighthouse:** not-installed
- **Config hash:** `66d5affe7c58723e4ac655a1f84bb03a09462311fe3575d311d58fc7897921d5`

## Methodology

- Parser reads **built HTML on disk** (not a JS DOM).
- JSON-LD from `<script type="application/ld+json">` via `json.loads`.
- URL corpus: `seo/benchmark/urls.txt` (35 sitemap URLs).
- GEO queries: `seo/benchmark/geo-queries.json` (observational only; no rank/citation claims).
- GEO rubric: `seo/benchmark/geo-rubric.md` (Stage 2 frozen 0–5, nine dimensions).
- Performance runtime (LCP/CLS/HAR-selected bytes) **not collected** — Lighthouse not installed; not added.

## Exact URL corpus

- https://maltstudio.co/
- https://maltstudio.co/hizmetler/
- https://maltstudio.co/hizmetler/tabela/
- https://maltstudio.co/bolgeler/tekirdag/
- https://maltstudio.co/projeler/
- https://maltstudio.co/projeler/ofiso/
- https://maltstudio.co/bilgi/
- https://maltstudio.co/bilgi/tabela-cesitleri/
- https://maltstudio.co/sektorler/
- https://maltstudio.co/sektorler/fabrika-osb/
- https://maltstudio.co/hizmetler/isikli-tabela/
- https://maltstudio.co/hizmetler/kutu-harf/
- https://maltstudio.co/hizmetler/totem/
- https://maltstudio.co/hizmetler/arac-giydirme/
- https://maltstudio.co/hizmetler/cam-giydirme/
- https://maltstudio.co/hizmetler/lightbox/
- https://maltstudio.co/hizmetler/display-pos/
- https://maltstudio.co/hizmetler/ofis-branding/
- https://maltstudio.co/hizmetler/is-guvenligi-tabelalari/
- https://maltstudio.co/projeler/yamanlar-ekspertiz/
- https://maltstudio.co/projeler/anka/
- https://maltstudio.co/projeler/kosem-doner/
- https://maltstudio.co/projeler/pembe-pasta-evi/
- https://maltstudio.co/projeler/okka-tarim/
- https://maltstudio.co/sektorler/restoran-cafe/
- https://maltstudio.co/sektorler/saglik/
- https://maltstudio.co/sektorler/plaza-ofis/
- https://maltstudio.co/sektorler/insaat-santiye/
- https://maltstudio.co/sektorler/perakende/
- https://maltstudio.co/bilgi/isikli-mi-isiksiz-mi/
- https://maltstudio.co/bilgi/kutu-harf-malzemeler/
- https://maltstudio.co/bilgi/one-way-vision-nedir/
- https://maltstudio.co/bilgi/arac-giydirme-rehberi/
- https://maltstudio.co/bilgi/tabela-fiyati/
- https://maltstudio.co/bilgi/totem-secim-rehberi/

## Metric definitions

- `word_count`: whitespace-split tokens in `<main>` (header/footer/nav excluded).
- `indexable`: robots meta does not contain `noindex`.
- `orphan candidate`: unreachable from homepage **inside this 35-URL graph** — not a global orphan.
- Image JPEG/WebP bytes: **on-disk** sizes of referenced files. Browser-selected transfer is unmeasured.

## GEO proxy (five-URL mean): **3.222** / 5

| URL | entity | answer | semantic | schema | machine | relations | trust | freshness | extract | mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `/` | 4 | 2 | 3 | 4 | 3 | 4 | 4 | 3 | 2 | 3.222 |
| `/hizmetler/tabela/` | 2 | 2 | 4 | 4 | 5 | 4 | 2 | 3 | 2 | 3.111 |
| `/bilgi/tabela-cesitleri/` | 2 | 5 | 5 | 4 | 5 | 4 | 2 | 4 | 4 | 3.889 |
| `/bolgeler/tekirdag/` | 2 | 2 | 3 | 4 | 5 | 4 | 4 | 3 | 2 | 3.222 |
| `/projeler/ofiso/` | 2 | 1 | 3 | 2 | 5 | 4 | 2 | 3 | 2 | 2.667 |

## Deterministic checks (fail = current AFTER gap)

- **TECHSEO-001** `live_robots_blocks_ai` = `['GPTBot', 'ClaudeBot', 'Google-Extended']` — pass = GPTBot/ClaudeBot/Google-Extended not Disallow / on live
- **TECHSEO-005** `gsc_meta` = `` — empty expected BEFORE
- **CONTENT-001** `project_wordcount_min` = `123` — {'https://maltstudio.co/projeler/ofiso/': 126, 'https://maltstudio.co/projeler/yamanlar-ekspertiz/': 123, 'https://maltstudio.co/projeler/anka/': 129, 'https://maltstudio.co/projeler/kosem-doner/': 129, 'https://maltstudio.co/projeler/pembe-pasta-evi/': 128, 'https://maltstudio.co/projeler/okka-tarim/': 129}
- **GEO-002** `md_twin_ratio_home` = `0.5428109854604201` — md=336 html=619

## Performance

Runtime Lighthouse/HAR: **not measured** (see `performance/`). Disk image evidence:
- Homepage JPEG fallback bytes (disk): 2286525
- Homepage WebP source bytes (disk): 1564562
- Homepage `<picture>` count: 6

## Sitemap / robots

- Git robots.txt exists: True; sitemap decl: ['https://maltstudio.co/sitemap.xml']
- Live robots fetched: True status=200
- Live AI bot Disallow / agents: []
- Sitemap locs: 37; missing lastmod: 0

## Crawl (corpus graph)

- Broken internal (sample): 0
- Unreachable from homepage in corpus: []
- Redirect rules hit from corpus links: 0

## External metrics unavailable locally

- LOCAL-001 GBP listing
- BRAND-001 LinkedIn entity (Jakarta collision) — not scraped
- EXTERNAL-001 SERP position
- ChatGPT / Perplexity / Gemini / AIO citations
- Lighthouse LCP/CLS/TBT and HAR-selected image bytes

## Known limitations

- Live HTTP timings are noise; not a scorecard.
- `www` redirect chain (TECHSEO-003) recorded only if probes succeeded.
- Python 3.9.6 local vs Cloudflare build 3.11 — parse results are encoding-stable JSON/HTML.

## Finding ID map

Every check row carries `finding_id`. GEO scores apply to SCHEMA-*, CONTENT-*, GEO-001/002, LOCAL-002.

