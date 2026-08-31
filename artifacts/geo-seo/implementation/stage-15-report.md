# Stage 15 — Custom domain cutover verified

**Outcome:** `STAGE 15 COMPLETE — PRODUCTION CUTOVER VERIFIED`

No application / SEO / schema / content / `robots.txt` / benchmark / `before/` changes. This commit is artifacts + this report only.

- **Production commit (Pages `main`):** `5c9789f` contains rebuild `c3335d8`
- **Public origin:** `https://maltstudio.co` now Cloudflare Pages (not Netlify)

---

## 1. `/hakkimizda/` headers

`GET https://maltstudio.co/hakkimizda/` → **HTTP 200**

- `x-nf-request-id`: **absent**
- `Netlify Edge`: **absent**
- `server: cloudflare`
- Title: `Hakkımızda | Malt Studio`

Same for the other sampled paths: no `x-nf-request-id`, no `Netlify Edge`.

---

## 2. Live HTTP (`maltstudio.co`)

| URL | Status | Notes |
|---|---|---|
| `/` | 200 | rebuild homepage JSON-LD |
| `/hizmetler/tabela/` | 200 | WebPage + Service + BreadcrumbList + FAQPage |
| `/bilgi/tabela-cesitleri/` | 200 | Article + BreadcrumbList |
| `/bolgeler/tekirdag/` | 200 | |
| `/projeler/ofiso/` | 200 | |
| `/hakkimizda/` | **200** | |
| `/gizlilik/` | 200 | |
| `/kvkk/` | **301** → `https://maltstudio.co/gizlilik/` | follow 200 |
| `/robots.txt` | 200 | CF Managed AI Disallow still present |
| `/sitemap.xml` | 200 | **37** loc; no `/admin/`, `/proje/`, `404.html`, `.md` |
| `/llms.txt` | 200 | |

`/404.html` → **308** `/404` with `x-robots-tag: noindex`, then 200. Not a Netlify 404.

`www.maltstudio.co` currently **200** on `/` (both custom domains Active). Previously Netlify 301’d www → apex. Not changed in git.

---

## 3. Live HTML (no JavaScript)

Homepage prerendered `#ld-json` includes:

- `#business` LocalBusiness + ProfessionalService
- `#website` / `#webpage`
- `geo`, `openingHoursSpecification`, `logo`, `image`, `knowsAbout`, `hasMap`
- `FAQPage`
- Instagram `sameAs` (`instagram.com/maltstudio.co`)

Guide: **Article** + WebPage + BreadcrumbList + FAQPage.

Tabela: title, description, self-canonical, OG, Twitter, Service + BreadcrumbList.

---

## 4. Robots

Live `https://maltstudio.co/robots.txt` still has `# BEGIN Cloudflare Managed content` with:

```
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /
```

**TECHSEO-001 — EXTERNAL — Cloudflare Managed AI Crawl Control**

Dashboard: **AI Crawl Control / Bot Preference Sync / Managed robots.txt** — Allow GPTBot, ClaudeBot, Google-Extended. Git `robots.txt` was not edited.

---

## 5. Collector

```
python3 scripts/seo/collect.py --out artifacts/geo-seo/live-stage-15 --phase AFTER
```

CLI only allows BEFORE/AFTER labels; snapshot directory is **`artifacts/geo-seo/live-stage-15/`**. Frozen 35-URL corpus. `before/` not written.

Collector scores repository HTML + **live** `robots.txt`. Independent live HTML fetch matches that schema, so LIVE equals repository AFTER.

```
AFTER captured SHA=5c9789f urls=35 geo_mean=3.133 fails=4
```

| | |
|---|---|
| GEO mean | **3.133 / 5** |
| Per URL | `/` 3.222 · tabela 3.000 · guide **3.778** · Tekirdağ 3.111 · ofiso 2.556 |
| Pass / fail / unscored | 39 pass · **4** fail · 2 unscored (GBP, LinkedIn) |
| Sitemap | 37 |
| Canonical | 35/35 self, absolute |
| Broken internal | **0** |
| JSON-LD parse | ok |

Fails (unchanged classification):

| ID | Class |
|---|---|
| TECHSEO-001 | EXTERNAL — live CF AI Disallow |
| TECHSEO-005 | EXTERNAL — empty GSC meta token |
| CONTENT-001 | INTENTIONAL — sparse project records (min 123 words) |
| GEO-002 | INTENTIONAL — homepage twin ratio 0.543 |

---

## BEFORE → AFTER → LIVE

| Phase | GEO | Fails |
|---|---|---|
| BEFORE | **2.333 / 5** | 26 |
| Repository AFTER | **3.133 / 5** | 4 |
| LIVE Stage 15 | **3.133 / 5** | 4 |

**Does `maltstudio.co` serve the 3.133 GEO rebuild?** Yes.

Not claimed (unmeasured): GBP, GSC HTML token, LinkedIn, SERP, AIO, ChatGPT/Perplexity/Gemini citations, Lighthouse/HAR.

Does `maltstudio.co` still reach Netlify? **No.**
