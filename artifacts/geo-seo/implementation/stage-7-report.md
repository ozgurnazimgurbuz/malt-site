# Stage 7 — GEO/SEO content & entity optimization

- **Branch:** `seo-rebuild`
- **HEAD:** `eec81da4a47dc77005eb64bab3cb2c63c931a3c2` (Stages 4–7 still uncommitted)
- **BEFORE artifacts:** frozen (`summary.json` sha256 `71f9c776…11364`)
- **KPI:** finding → measure → BEFORE → impl → AFTER. Not the original 45/100.

Stage 6 AFTER: GEO mean **2.956**, **6** failing checks.

Stage 7 AFTER (same collector, recaptured): GEO mean **3.133**, **4** failing checks.

No commit/push.

---

## Scoreboard

| URL | Stage 6 | Stage 7 |
|---|---|---|
| `/` | 3.222 | **3.222** |
| `/hizmetler/tabela/` | 3.000 | **3.000** |
| `/bilgi/tabela-cesitleri/` | 3.111 | **3.778** |
| `/bolgeler/tekirdag/` | 2.889 | **3.111** |
| `/projeler/ofiso/` | 2.556 | **2.556** |
| **GEO mean** | **2.956** | **3.133** |

CONTENT-003 `guide_passage_80_160` and `comparison_table` now **PASS**. Remaining fails are the Stage 6 external/intentional set.

---

## Remaining Failure Disposition

| Check | Classification | Action |
|---|---|---|
| TECHSEO-001 live CF AI Disallow | EXTERNAL_LIMITATION | No local change |
| TECHSEO-005 empty GSC | EXTERNAL_LIMITATION | No token in repo |
| CONTENT-001 project &lt;400 words | INTENTIONAL_BEHAVIOR | Honest proje kaydı; no invented case study |
| GEO-002 home md twin ratio 0.460 | INTENTIONAL_BEHAVIOR | Homepage twin stays a curated extract. New FAQ grew HTML; twin was not padded |

---

## Genuine fixes

### Related projects actually render

- `related_rail` used an empty name map, so project cards never appeared. `portfolio_names()` now reads live `content.json` slugs.
- `SERVICE_DEPTH.related_projects` pointed at 410 placeholders (`volt-enerji`, `liman-kahve`, …). Mapped only to CMS portfolio: ofiso, yamanlar-ekspertiz, pembe-pasta-evi, anka, kosem-doner, okka-tarim. Araç giydirme / lightbox / display-pos stay empty. Fabrika & OSB stays empty (no OSB case in CMS).

### Service pages

- Shared “Teklif öncesi ne paylaşın?” checklist from existing process facts (photo, ölçü, gece ihtiyacı, logo). No prices.
- FAQ answers expanded to actually answer; path-only answers became `<a href>`. FAQPage uses the same pairs (`visible_text` strips tags).
- Guide rail titles use article titles, not generic “Rehber”.
- Ofis branding typo `sahiplenır` → `sahiplenir`.

### Guides

- Comparison tables on `tabela-cesitleri`, `isikli-mi-isiksiz-mi`, `kutu-harf-malzemeler` — qualitative only, linking related services. Not added to non-comparison guides.
- Intro passages on the two comparison guides are 97 / 91 words (collector 80–160 band). Content is the same type distinctions already in the repo, not filler.
- Path-only “sipariş?” FAQ answers became real links.

### Tekirdağ / entity

- All 10 public services listed (not only A0).
- CMS `googleMapsUrl` as koordinat araması; explicitly not a Place ID / GBP claim.
- CMS Instagram URL on the atölye page.
- FAQs: hours, address, hizmet listesi, çevre ilçeler.
- `llms.txt` NAP: street + hours + Instagram + both phone forms.
- `content.json` category typo `Restorant` → `Restoran`.
- Hakkımızda now states hours in the same wording as the atölye page.
- Homepage FAQ adds working hours; prerender FAQPage has 5 matching `<details>`.

### Machine-readable twins

- `build_llms.py` emits Markdown tables (`td`/`th`) so twins match visible comparison structure.

---

## Not done (on purpose)

- Project pages not padded to 400 words.
- No LinkedIn, YouTube, GBP, invented customers, prices, or coverage cities.
- Frozen BEFORE, `seo/benchmark/urls.txt`, `geo-queries.json`, `geo-rubric.md` untouched.
- Homepage md twin not inflated (GEO-002 remains fail).

---

## Tests

```
python3 scripts/seo/test_schema.py          # schema self-check ok
python3 scripts/seo/test_collect.py        # seo collector self-check ok
python3 scripts/test_project_tracking.py  # PASS (5 suites)
python3 scripts/seo/collect.py --out artifacts/geo-seo/after --phase AFTER
```

Local HTTP smoke: `/bilgi/isikli-mi-isiksiz-mi/` 200 + `<table>`; `/hizmetler/tabela/` 200 + `/projeler/ofiso/`; `/bolgeler/tekirdag/` 200 + Instagram.

Browser MCP was unavailable; verification used curl + HTML/JSON-LD inspection instead.
