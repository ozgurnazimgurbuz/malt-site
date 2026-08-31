# GEO/SEO benchmark harness (Stage 3)

Measurement only. Does not modify production HTML, schema, content, or deploy config.

**Base URL:** `https://maltstudio.co`

## Commands

```bash
python3 scripts/seo/collect.py
python3 scripts/seo/test_collect.py
```

Makefile aliases (optional):

```bash
make seo-before
make seo-test
```

## Frozen inputs (do not edit after BEFORE)

| File | Role |
|---|---|
| `urls.txt` | 35 public sitemap URLs |
| `geo-queries.json` | Observational query groups (no ranking claims) |
| `geo-rubric.md` | Stage 2 0–5 rubric |

## Output

`artifacts/geo-seo/before/`

Parser reads **built HTML on disk**. JSON-LD is taken from HTML source, not a JS-executed DOM.

## Not installed

Lighthouse / Playwright / Node are not part of this repo. Do not add them for this harness.
