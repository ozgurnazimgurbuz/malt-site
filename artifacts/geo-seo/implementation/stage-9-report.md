# Stage 9 — Final GEO gap resolution & external readiness

- **Branch:** `seo-rebuild`
- **HEAD:** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2` (Stages 4–9 still uncommitted)
- **BEFORE artifacts:** frozen (`summary.json` sha256 `71f9c77685878d873be07f06610aada4912b9eac79e086a753cf59b9ec711364`)
- **KPI:** finding → measure → BEFORE → impl → AFTER.

Stage 8 AFTER: GEO mean **3.133**, **4** failing checks.

Stage 9 AFTER: GEO mean **3.133**, **4** failing checks (same four; not “solved”).

This stage is a decision/readiness pass. No padding, no invented tokens, no Cloudflare edits, no fabricated GBP/LinkedIn/SERP.

No commit/push.

---

## 1. The four remaining failures

| ID | Metric | Classification | Evidence |
|---|---|---|---|
| TECHSEO-001 | `live_robots_blocks_ai` | **External limitation** | Git `robots.txt` Allows `/` and only Disallows `/admin/`, `/proje/`. Live `https://maltstudio.co/robots.txt` prepends `# BEGIN Cloudflare Managed content` with `User-agent: GPTBot\|ClaudeBot\|Google-Extended` + `Disallow: /`. Collector pass = those three UAs not `Disallow: /` on **live**. Cannot be fixed in this repo. |
| TECHSEO-005 | `gsc_meta` | **External limitation** | `content.json` `"googleSearchConsoleVerification": ""`. Homepage has no `<meta name="google-site-verification">`. Token does not exist in the repo. Do not invent one. |
| CONTENT-001 | `project_wordcount_min` ≥ 400 | **Intentional behavior** | All 6 CMS portfolio items have empty `description`, `year`, `client`, `completedDate`, `gallery`. `build_production.py` only renders filled fields. Min word count **123** (Yamanlar 123 … Anka/Köşem/Okka 129). Padding would fabricate case studies. |
| GEO-002 | `md_twin_ratio_home` ≥ 0.70 | **Intentional / curated** | Homepage HTML **619** words (nav/footer included in collector count). Twin is a main-content extract. After Stage 9 parseability work: **336 / 619 = 0.543**. Still below 0.70. Inflating the twin to hit the ratio would duplicate chrome, not add facts. `llms.txt` is the curated AI index. |

None of these are obsolete assertions. Benchmark criteria were left unchanged.

---

## 2. Homepage machine-readable content

`llms.txt` already has NAP, both phone forms, hours, Instagram, no fake claims. Sufficient as the entity index.

Genuine repo gap (not ratio gaming): `_MdConverter` glued service-card innards (`01TabelaDış…`) and emitted empty `###` because `<h3>`/`<div>` inside `<a>` did not insert spaces. Homepage twin also omitted NAP because `extract_main_html` strips `<footer>`.

**Done (useful, not padded):**

- Converter: space between block children inside links; collapse whitespace; `<br>` → space (so `Bilgi<br> Merkezi` stays one heading).
- Homepage twin: short **İletişim** stanza from CMS (email, both phone forms, address, hours, Instagram). Same facts as `llms.txt` / footer.
- Word count 285 → 336. Ratio 0.46 → **0.543**. Still FAIL GEO-002, on purpose.

No further twin enlargement.

---

## 3. Project content

CMS portfolio fields that exist: `name`, `slug`, `location` (Tekirdağ), `services`, `category`, `image`, `featured`.

Empty on every item: `client`, `description`, `year`, `completedDate`, `gallery`.

`build_production.py` already exposes only filled fields (`if client:` / `if year:` / `if completed:` / `if description:`). Sparse records stay short pages with name, location, category, services, photos.

**Decision preserved:** do not pad to 400 words. CONTENT-001 remains an intentional fail.

Private `/proje/` tracking records (`clientName`, steps) are `noindex` + robots Disallow. They are not public case studies.

---

## 4. External readiness (do not execute from git)

### Cloudflare — TECHSEO-001

Live file (`artifacts/geo-seo/after/raw/robots-live.txt`) prepends managed Disallow for: Amazonbot, Applebot-Extended, Bytespider, CCBot, **ClaudeBot**, CloudflareBrowserRenderingCrawler, **Google-Extended**, **GPTBot**, meta-externalagent.

Git `robots.txt` must stay as-is (`Allow: /` + private Disallows). Changing it does not change the live prepend.

**What to change in the Cloudflare dashboard (not in this repo):**

1. Zone `maltstudio.co` → **AI Crawl Control** → Crawlers → set **Allow** for **GPTBot**, **ClaudeBot**, **Google-Extended**.
2. Stop the managed robots prepend from rewriting those three as `Disallow: /`. That block is `# BEGIN Cloudflare Managed content` … `# END`. It comes from Bot Preference Sync / Managed robots.txt, not from git. Either:
   - set Search/Agent access so those crawlers are not written as `Disallow: /`, or
   - turn off Bot Preference Sync / managed robots.txt so origin `robots.txt` is served as committed.
3. Confirm by fetching `https://maltstudio.co/robots.txt`: those three UAs must not have `Disallow: /`.
4. Optional: keep `Content-Signal: search=yes,ai-train=no,use=reference`. Collector does not score that; it only fails on `Disallow: /` for the three GEO agents.

Do not modify Cloudflare from this repository.

### Google Search Console — TECHSEO-005

**Where the token belongs:**

1. Decap: `admin/config.yml` field **Google Search Console Doğrulama Kodu** → `googleSearchConsoleVerification`.
2. Stored in `content.json` → `googleSearchConsoleVerification`.
3. `scripts/prerender.py` now emits `<meta name="google-site-verification" content="…">` **only when the field is non-empty**. Empty → no tag (current state).

After a real token exists: paste it in CMS, rebuild/prerender, deploy. Client JS (`upsertMeta`) only runs when the homepage is **not** prerendered; crawlers need the prerendered tag.

Do not invent a token. Check stays FAIL until a real value is saved.

### Google Business Profile

Repo already has enough to **later attach** a GBP entity. It does **not** prove one exists.

| Field | Value in repo |
|---|---|
| Name | Malt Studio |
| Address | Yavuz Mahallesi, Ruşen Güneş Sokak, D Blok No:2, 59100 Süleymanpaşa / Tekirdağ |
| Geo | `40.9769375`, `27.5041875` |
| `googleMapsUrl` / `hasMap` | `https://www.google.com/maps/search/?api=1&query=40.9769375,27.5041875` (coordinate search, **not** a Place ID) |
| Hours | Mon–Sat 09:00–19:00 |
| Phone | `+905525826959` / display `+90 552 582 69 59` |
| Instagram | `https://www.instagram.com/maltstudio.co/` |

Collector: `hasMap` PASS with detail `CMS googleMapsUrl coordinate search; not a GBP Place ID`. `gbp_place_id` is unscored EXTERNAL.

Future: replace `googleMapsUrl` with a real Place URL/ID once GBP is verified. Do not claim ownership now.

### LinkedIn

`content.json` `"linkedin": ""`. `sameAs` is Instagram-only. `test_schema.py` asserts Jakarta `linkedin.com/company/malt-studio` is absent.

Do not add a LinkedIn URL. There is still no trustworthy company page in this repo.

---

## 5. Entity consistency (final cross-check)

No contradictory identity found.

| Fact | CMS / HTML / schema / llms / twin |
|---|---|
| Name | Malt Studio |
| Domain | `https://maltstudio.co` |
| Email | merhaba@maltstudio.co |
| Phone | `05525826959` = `+90 552 582 69 59` = `tel:+905525826959` = WhatsApp `905525826959` |
| Address | Yavuz Mahallesi, Ruşen Güneş Sokak, D Blok No:2, 59100 Süleymanpaşa / Tekirdağ, TR |
| Geo | 40.9769375, 27.5041875 |
| Hours | Pazartesi–Cumartesi 09:00–19:00 |
| Instagram | `https://www.instagram.com/maltstudio.co/` (schema `sameAs`, llms, twin, Tekirdağ page). Homepage footer link exists but is `hidden` — visibility choice, not a different URL. |
| LinkedIn | empty everywhere |
| Logo | CMS `"logo": ""`; schema uses `https://maltstudio.co/images/icon-512.png` |
| Services | 15 homepage cards; `schemaServices` / `knowsAbout` is the 10-item catalog. Compatible, not contradictory. |
| Tekirdağ | `addressRegion`, hero, `/bolgeler/tekirdag/`, all 6 projects `location: Tekirdağ` |
| Maps | coordinate search only |

---

## 6. Tests & AFTER recapture

```
python3 scripts/seo/test_schema.py          # schema self-check ok
python3 scripts/seo/test_collect.py        # seo collector self-check ok
python3 scripts/test_project_tracking.py  # PASS (5 suites)
python3 scripts/seo/collect.py --out artifacts/geo-seo/after --phase AFTER
```

AFTER: `geo_mean=3.133` `fails=4` SHA=`eec81da`.

BEFORE checksum unchanged.

---

## Repo-controlled work in this stage

| Change | Why |
|---|---|
| `scripts/build_llms.py` converter spacing + homepage NAP stanza | AI-parseable twins; facts already in CMS |
| `scripts/prerender.py` GSC meta if token present | Wiring for a future real token |
| `scripts/seo/test_schema.py` | Converter + empty-GSC checks |
| Regenerated `*.md`, `llms.txt`, `llms-full.txt` | Output of converter |

Not done (on purpose): project padding, twin ratio 0.70, invented GSC/CF/GBP/LinkedIn, benchmark edits.

---

## Verdict

Nothing genuinely useful remains **inside the repository** for those four fails.

Remaining GEO movement is **external**:

1. Cloudflare: Allow GPTBot / ClaudeBot / Google-Extended (and stop managed `Disallow: /`).
2. GSC: paste a real verification token into CMS, rebuild, deploy.
3. GBP: create/verify off-site, then optionally point `googleMapsUrl` at a Place ID.
4. LinkedIn: only if a real Malt Studio company URL exists — never the Jakarta slug.
5. Project copy: only if Özgür writes real client/date/description into CMS.

Site is technically sound. GEO mean **3.133 / 5** is the honest ceiling until those external items exist.
