# GEO/SEO BEFORE baseline

- **BEFORE SHA:** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2`
- **Branch:** `main`
- **Benchmark date:** 2026-08-30T21:15:34Z
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

## GEO proxy (five-URL mean): **2.333** / 5

| URL | entity | answer | semantic | schema | machine | relations | trust | freshness | extract | mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `/` | 3 | 2 | 3 | 2 | 3 | 1 | 2 | 2 | 2 | 2.222 |
| `/hizmetler/tabela/` | 2 | 2 | 4 | 2 | 4 | 3 | 2 | 2 | 2 | 2.556 |
| `/bilgi/tabela-cesitleri/` | 2 | 2 | 3 | 0 | 4 | 2 | 2 | 1 | 3 | 2.111 |
| `/bolgeler/tekirdag/` | 2 | 2 | 3 | 2 | 4 | 3 | 2 | 2 | 2 | 2.444 |
| `/projeler/ofiso/` | 2 | 1 | 3 | 2 | 4 | 3 | 2 | 2 | 2 | 2.333 |

## Deterministic checks (fail = current BEFORE gap)

- **SCHEMA-001** `home_ld_has_website` = `False` — types=['LocalBusiness', 'ProfessionalService']
- **SCHEMA-001** `home_ld_geo` = `False` — geo on #business
- **SCHEMA-001** `home_ld_hours` = `False` — 
- **SCHEMA-001** `home_ld_logo` = `False` — 
- **SCHEMA-001** `home_ld_knowsAbout_ge3` = `0` — []
- **LOCAL-002** `home_ld_geo_hours` = `{'geo': False, 'hours': False}` — same patch as SCHEMA-001
- **SCHEMA-002** `website_node_defined_on_home` = `False` — inner refs require homepage definition
- **SCHEMA-003** `faqpage_parity_home` = `{'html_faq': 4, 'faqpage': False}` — FAQPage must match visible details
- **SCHEMA-003** `faqpage_parity_tabela` = `{'html_faq': 8, 'faqpage': False}` — 
- **SCHEMA-004** `guides_sectors_have_jsonld` = `False` — ['https://maltstudio.co/bilgi/', 'https://maltstudio.co/bilgi/tabela-cesitleri/', 'https://maltstudio.co/sektorler/', 'https://maltstudio.co/sektorler/fabrika-osb/', 'https://maltstudio.co/sektorler/restoran-cafe/', 'https://maltstudio.co/sektorler/saglik/', 'https://maltstudio.co/sektorler/plaza-ofis/', 'https://maltstudio.co/sektorler/insaat-santiye/', 'https://maltstudio.co/sektorler/perakende/', 'https://maltstudio.co/bilgi/isikli-mi-isiksiz-mi/', 'https://maltstudio.co/bilgi/kutu-harf-malzemeler/', 'https://maltstudio.co/bilgi/one-way-vision-nedir/', 'https://maltstudio.co/bilgi/arac-giydirme-rehberi/', 'https://maltstudio.co/bilgi/tabela-fiyati/', 'https://maltstudio.co/bilgi/totem-secim-rehberi/']
- **SCHEMA-005** `sameAs` = `['https://www.instagram.com/maltstudio.co/']` — Instagram-only expected BEFORE; LinkedIn empty in CMS
- **TECHSEO-001** `live_robots_blocks_ai` = `['GPTBot', 'ClaudeBot', 'Google-Extended']` — pass = GPTBot/ClaudeBot/Google-Extended not Disallow / on live
- **TECHSEO-002** `sitemap_all_lastmod` = `15` — ['https://maltstudio.co/sektorler/', 'https://maltstudio.co/bilgi/', 'https://maltstudio.co/sektorler/fabrika-osb/', 'https://maltstudio.co/sektorler/restoran-cafe/', 'https://maltstudio.co/sektorler/saglik/', 'https://maltstudio.co/sektorler/plaza-ofis/', 'https://maltstudio.co/sektorler/insaat-santiye/', 'https://maltstudio.co/sektorler/perakende/', 'https://maltstudio.co/bilgi/tabela-cesitleri/', 'https://maltstudio.co/bilgi/isikli-mi-isiksiz-mi/', 'https://maltstudio.co/bilgi/kutu-harf-malzemeler/', 'https://maltstudio.co/bilgi/one-way-vision-nedir/', 'https://maltstudio.co/bilgi/arac-giydirme-rehberi/', 'https://maltstudio.co/bilgi/tabela-fiyati/', 'https://maltstudio.co/bilgi/totem-secim-rehberi/']
- **TECHSEO-005** `gsc_meta` = `` — empty expected BEFORE
- **SEO-001** `og_image_alt_not_stale` = `Malt Studio — Marka Stratejisi ve Yaratıcı Ajans` — Malt Studio — Marka Stratejisi ve Yaratıcı Ajans
- **SEO-002** `h2_br_space_sektorler` = `True` — Çalıştığımız<br>Sektörler concat
- **SEO-002** `h2_br_space_bilgi` = `True` — 
- **PERF-002** `first_work_img_lazy` = `True` — first work-item img loading attr
- **CONTENT-001** `project_wordcount_min` = `95` — {'https://maltstudio.co/projeler/ofiso/': 98, 'https://maltstudio.co/projeler/yamanlar-ekspertiz/': 95, 'https://maltstudio.co/projeler/anka/': 101, 'https://maltstudio.co/projeler/kosem-doner/': 101, 'https://maltstudio.co/projeler/pembe-pasta-evi/': 99, 'https://maltstudio.co/projeler/okka-tarim/': 101}
- **CONTENT-002** `eeat_clone_pages` = `27` — ['https://maltstudio.co/hizmetler/', 'https://maltstudio.co/hizmetler/tabela/', 'https://maltstudio.co/projeler/', 'https://maltstudio.co/bilgi/', 'https://maltstudio.co/bilgi/tabela-cesitleri/', 'https://maltstudio.co/sektorler/', 'https://maltstudio.co/sektorler/fabrika-osb/', 'https://maltstudio.co/hizmetler/isikli-tabela/', 'https://maltstudio.co/hizmetler/kutu-harf/', 'https://maltstudio.co/hizmetler/totem/', 'https://maltstudio.co/hizmetler/arac-giydirme/', 'https://maltstudio.co/hizmetler/cam-giydirme/', 'https://maltstudio.co/hizmetler/lightbox/', 'https://maltstudio.co/hizmetler/display-pos/', 'https://maltstudio.co/hizmetler/ofis-branding/', 'https://maltstudio.co/hizmetler/is-guvenligi-tabelalari/', 'https://maltstudio.co/sektorler/restoran-cafe/', 'https://maltstudio.co/sektorler/saglik/', 'https://maltstudio.co/sektorler/plaza-ofis/', 'https://maltstudio.co/sektorler/insaat-santiye/', 'https://maltstudio.co/sektorler/perakende/', 'https://maltstudio.co/bilgi/isikli-mi-isiksiz-mi/', 'https://maltstudio.co/bilgi/kutu-harf-malzemeler/', 'https://maltstudio.co/bilgi/one-way-vision-nedir/', 'https://maltstudio.co/bilgi/arac-giydirme-rehberi/', 'https://maltstudio.co/bilgi/tabela-fiyati/', 'https://maltstudio.co/bilgi/totem-secim-rehberi/']
- **CONTENT-003** `guide_passage_80_160` = `0` — max_p=53
- **CONTENT-003** `comparison_table` = `0` — 
- **CONTENT-004** `about_page` = `False` — absence is trust gap, not crawl bug
- **CONTENT-005** `kvkk_or_privacy` = `False` — []
- **GEO-002** `md_twin_ratio_home` = `0.47738693467336685` — md=285 html=597
- **LOCAL-001** `hasMap_or_gbp` = `False` — EXTERNAL GBP not measured here

## Performance

Runtime Lighthouse/HAR: **not measured** (see `performance/`). Disk image evidence:
- Homepage JPEG fallback bytes (disk): 2286525
- Homepage WebP source bytes (disk): 1564562
- Homepage `<picture>` count: 6

## Sitemap / robots

- Git robots.txt exists: True; sitemap decl: ['https://maltstudio.co/sitemap.xml']
- Live robots fetched: True status=200
- Live AI bot Disallow / agents: ['GPTBot', 'ClaudeBot', 'Google-Extended']
- Sitemap locs: 35; missing lastmod: 15

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

