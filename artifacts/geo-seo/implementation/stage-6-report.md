# Stage 6 — Deterministic gap closure

- **Branch:** `seo-rebuild`
- **HEAD:** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2` (Stage 4+6 still uncommitted)
- **BEFORE artifacts:** frozen, checksum unchanged
- **KPI:** finding → measure → BEFORE → impl → AFTER. Not the original 45/100.

Stage 5 AFTER (collector, pre–Stage 6): GEO mean **2.956**, **10** failing checks.

Stage 6 AFTER (same collector, recaptured): GEO mean **2.956**, **6** failing checks, **2** unscored external.

No commit/push.

---

## Remaining Failure Disposition

Original Stage 5 ten failures:

| Check | Finding ID | Failure | Classification | Reason | Action | Final |
|---|---|---|---|---|---|---|
| `sameAs` hardcoded fail | SCHEMA-005 | Instagram present; check always `pass=False` | `OBSOLETE_ASSERTION` | Instagram is the real CMS `sameAs`. Jakarta LinkedIn must stay absent (`BRAND-001`). Hardcoded fail was a BEFORE snapshot, not an invariant. | Pass when Instagram is present and Jakarta slug is absent | **PASS** |
| `live_robots_blocks_ai` | TECHSEO-001 | Live CF Disallow `/` for GPTBot, ClaudeBot, Google-Extended | `EXTERNAL_LIMITATION` | Git `robots.txt` does not block those agents. Live file is Cloudflare-managed. Repo must not spoof CF. | No local change | **FAIL** (live) |
| `sitemap_url_count == 35` | TECHSEO-002 | Sitemap 37 after `/gizlilik/` + `/hakkimizda/` | `OBSOLETE_ASSERTION` | Count equality is not an SEO invariant. Public coverage / uniqueness / no private URLs are. | Replaced with required-public, unique, no-private, absolute-https | **PASS** (37 listed, 37 required) |
| `gsc_meta` empty | TECHSEO-005 | No Search Console verification meta | `EXTERNAL_LIMITATION` | Token is not in the repo. Do not invent one. | No local change | **FAIL** |
| `project_wordcount_min >= 400` | CONTENT-001 | Min 123 words | `INTENTIONAL_BEHAVIOR` | Stage 4 used honest “proje kaydı” copy. Padding to 400 would fabricate case studies. | No content invention | **FAIL** |
| `eeat_clone_pages` 27 | CONTENT-002 | Same “Üretim, deneyim ve yerel uzmanlık” block on 27 URLs | `GENUINE_GAP` | Duplicated boilerplate, not unique evidence. Deletion does not invent E-E-A-T. | Removed `eeat_block()` from inner templates | **PASS** (0 pages) |
| `guide_passage_80_160` | CONTENT-003 | max paragraph 53 words | `EXPECTED_STATE` | Guides are short cards/lists. Writing 80–160w passages would be new copy for the score. | No fabrication | **FAIL** |
| `comparison_table` | CONTENT-003 | No `<table>` on ışıklı vs ışıksız | `EXPECTED_STATE` | Comparison exists as lists. Adding a table would be GEO-score markup. | No table added | **FAIL** |
| `md_twin_ratio_home >= 0.70` | GEO-002 | md 285 / html 599 ≈ 0.476 | `INTENTIONAL_BEHAVIOR` | Homepage twin is curated `llms` extract, not a full DOM dump. Inflating the twin would game machine-readability. | No twin padding | **FAIL** |
| `hasMap_or_gbp` hardcoded fail | LOCAL-001 | `hasMap` true after Stage 4; check always `pass=False` | `OBSOLETE_ASSERTION` + `EXTERNAL_LIMITATION` | Coordinate `hasMap` is first-party CMS. GBP Place ID is not in repo and must not be claimed. | Split: `hasMap` pass; `gbp_place_id` unscored | **PASS** hasMap · GBP **unscored** |

Footer warning `build_home_a3: footer columns pattern not found`: **EXPECTED_STATE**. Homepage footer uses `<h3>`; A3 regex looks for `<h4>`. Skip does not remove `/gizlilik/` or `/hakkimizda/` (verified in `index.html`). Production behavior not changed to silence the warn.

---

## Genuine Fixes

### CONTENT-002 — cloned EEAT block

- **Files:** `scripts/build_production.py` (stopped emitting `eeat_block()` on hizmet, bilgi, sektör, proje hub, Tekirdağ). `lib_site.eeat_block` left unused.
- **Reason:** One honest paragraph cloned onto 27 URLs. Hakkımızda already states the same facts without that H2 fingerprint.
- **Validation:** collector `eeat_clone_pages` 27 → **0**. Fingerprint absent from `hizmetler/tabela/index.html`. Schema types unchanged.

### TECHSEO-002 — sitemap invariants

- **Files:** `scripts/seo/collect.py`, `scripts/seo/test_collect.py`
- **Reason:** `count == 35` failed because two intentional public pages were added. A real regression is a missing public URL, a duplicate loc, a private/noindex loc, or a non-absolute loc.
- **New checks:** `sitemap_required_public` (frozen 35 + `/gizlilik/` + `/hakkimizda/`), `sitemap_unique`, `sitemap_no_private`, `sitemap_absolute_https`. Count is informational (`required=37 listed=37`).
- **Validation:** all four pass. `404.html` and `/proje/` still absent from sitemap.

### SCHEMA-005 — Instagram `sameAs`

- **Files:** `scripts/seo/collect.py`
- **Reason:** Hardcoded fail ignored a correct Instagram URL.
- **Validation:** pass. Jakarta LinkedIn still absent (`BRAND-001` still pass).

### LOCAL-001 — hasMap vs GBP

- **Files:** `scripts/seo/collect.py`
- **Reason:** `hasMap` is the CMS coordinate search URL. GBP remains unmeasured.
- **Validation:** `hasMap` pass; `gbp_place_id` `pass=null`.

### Collector `--out` / `--phase`

- **Files:** `scripts/seo/collect.py`
- **Reason:** Default still writes `artifacts/geo-seo/before/`. Stage 6 recapture used `--out artifacts/geo-seo/after --phase AFTER` so BEFORE stayed frozen.

---

## Expected / External Items

Cannot be solved locally without fabrication or dashboard access:

| Item | Status |
|---|---|
| Cloudflare AI crawler Disallow | EXTERNAL — live `robots.txt` still blocks GPTBot / ClaudeBot / Google-Extended |
| GSC verification meta | EXTERNAL — empty |
| GBP Place ID / reviews | EXTERNAL — hasMap is not GBP |
| LinkedIn | EXTERNAL — CMS empty; Jakarta URL forbidden |
| SERP / AIO / ChatGPT / Perplexity / Gemini citations | EXTERNAL |
| Lighthouse LCP/CLS/TBT/HAR | NOT MEASURED — no Node/Lighthouse |
| 400-word case studies | INTENTIONAL — no invented project narrative |
| 80–160w guide passages + comparison `<table>` | EXPECTED — existing short educational copy kept |
| Homepage md twin ratio | INTENTIONAL — curated twin |

Local deterministic implementation for schema/metadata/sitemap/indexability is complete relative to first-party data.

---

## Regression Analysis

### Stage 5 AFTER → Stage 6 AFTER

| Signal | Stage 5 | Stage 6 | Notes |
|---|---|---|---|
| GEO mean | 2.956 | 2.956 | Unchanged (rubric not targeted) |
| Failing collector checks | 10 | 6 | 4 closed (obsolete + clone) |
| Homepage JSON-LD types | FAQPage, LB, PS, WebPage, WebSite | same | |
| hasMap / geo / hours / logo / knowsAbout | present | same | |
| FAQPage parity | 25/25 | same | |
| Article on `/bilgi/{slug}/` | yes | same | |
| Canonicals (corpus) | 35/35 self | 35/35 self | |
| Accidental noindex | none | none | |
| Sitemap | 37, all lastmod | 37, invariants pass | |
| Broken internal | [] | [] | |
| `/proje/` robots + noindex | kept | kept | |
| `404.html` noindex, not in sitemap | yes | yes | |
| Home JPEG/WebP disk bytes | 2,286,525 / 1,564,562 | same | |
| `<picture>` count | 6 | 6 | |
| First work img lazy | false | same | |
| Tabela word_count | 662 | 562 | EEAT block removed |
| Guide `/bilgi/tabela-cesitleri/` words | 556 | 457 | same deletion |
| `llms-full.txt` | ~178 KB | 155,708 B | twins no longer repeat the clone |
| Footer gizlilik/hakkimizda | present | present | |
| Jakarta LinkedIn | absent | absent | |

No schema, canonical, robots, sitemap-loss, private-route leakage, or image-architecture regression.

Inner-page word counts dropped by the cloned EEAT section only. Unique service/guide copy remains. That is the intended deletion, not a content hole.

### BEFORE → Stage 6

GEO 2.333 → **2.956**. Collector fails 26 → **6**. Homepage graph, FAQPage, Article, lastmod, OG alt, legal pages, 404, hasMap, first-work eager image: still in place from Stage 4.

---

## GEO rubric (frozen five) — remaining weakness

Rubric unchanged. Scores Stage 5 AFTER = Stage 6 AFTER.

| URL | entity | answer | semantic | schema | machine | relations | trust | freshness | extract | mean |
|---|---|---|---|---|---|---|---|---|---|---|
| `/` | 4 | 2 | 3 | 4 | 3 | 4 | 4 | 3 | 2 | 3.222 |
| `/hizmetler/tabela/` | 2 | 2 | 4 | 4 | 4 | 4 | 2 | 3 | 2 | 3.000 |
| `/bilgi/tabela-cesitleri/` | 2 | 2 | 3 | 4 | 4 | 4 | 2 | 4 | 3 | 3.111 |
| `/bolgeler/tekirdag/` | 2 | 2 | 3 | 4 | 4 | 4 | 2 | 3 | 2 | 2.889 |
| `/projeler/ofiso/` | 2 | 1 | 3 | 2 | 4 | 4 | 2 | 3 | 2 | 2.556 |

Why they stay low (not local schema bugs):

- **Answerability 1–2:** FAQ answers are 1–2 sentences. Longer answers would be new copy.
- **Extractability 2–3:** cards/short paragraphs; 400-word projects and 80–160w passages absent by choice.
- **Entity clarity 2 on inner pages:** LocalBusiness lives on the homepage `#business` `@id`. Inner pages do not duplicate the entity (avoids duplicate LocalBusiness). Residual `#business` dangling on inner graphs is that design.
- **Trust 2 on inner pages:** hours+maps are homepage/NAP; inner pages have legal footer links but not hours+maps HTML.
- **ofiso structured data 2:** no FAQPage (no visible FAQ). Dangling `#business` only.
- **GBP / LinkedIn / live AI bots:** external; not encoded into these integers beyond live-bot machine_readability.

`/hizmetler/ofis-tabelasi/` still does not exist. Frozen fifth URL remains `/projeler/ofiso/`.

---

## Schema / technical / performance (Stage 6 inspect)

Homepage `#business`: LocalBusiness + ProfessionalService, geo, hours, logo, image, description, knowsAbout (15), hasMap (coordinate search), Instagram `sameAs`, `#website`, `#webpage`, FAQPage matching 4 visible `<details>`. `duplicate_ids` empty. Dual type on one `@id` is the same as BEFORE, not two nodes.

Inner: Service + WebPage + BreadcrumbList + WebSite node; guides add Article + FAQPage. FAQ schema still matches visible pairs. No extra schema added for score.

Public corpus: one absolute self-canonical each; no accidental noindex. Git robots still Disallow `/admin/` and `/proje/`. Tracking pages `noindex, nofollow`. Redirects: `/kvkk` → `/gizlilik/` in `_redirects` only (live origin not Stage 6).

Performance: disk JPEG/WebP unchanged. No image architecture rewrite.

---

## Final Deterministic State

| | Count |
|---|---:|
| Total collector checks | 45 (6 fail + 37 pass + 2 unscored) |
| Passing | 37 |
| Failing (local content + live/external tokens) | 6 |
| Unscored external | 2 (`LOCAL-001 gbp_place_id`, `EXTERNAL-001` SERP) |
| GEO mean | **2.956 / 5** |
| Per-URL GEO | `/` 3.222 · tabela 3.000 · tabela-cesitleri 3.111 · tekirdag 2.889 · ofiso 2.556 |

Remaining fails: TECHSEO-001 (live CF), TECHSEO-005 (GSC), CONTENT-001 (project length), CONTENT-003 ×2, GEO-002 (home twin). None of those are broken generators.

---

## Git state (no commit)

- **Branch:** `seo-rebuild` (tracks `origin/seo-rebuild`)
- **HEAD:** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2`
- **Working tree:** dirty (Stage 4 + Stage 6 HTML regeneration + collector). `scripts/seo/` still untracked from Stage 3.
- Stage 6 source edits: `scripts/build_production.py`, `scripts/seo/collect.py`, `scripts/seo/test_collect.py`, regenerated inner HTML/md, `artifacts/geo-seo/after/`, this report.

`git diff --stat` (tracked files, includes Stage 4+6): **80 files, +969 / −989**.
