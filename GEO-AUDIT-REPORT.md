# GEO Audit Report: Malt Studio

**Audit Date:** 30 August 2026
**URL:** https://maltstudio.co/
**Business Type:** Hybrid — Local Business + Agency/Services (Tekirdağ tabela üretimi ve reklam uygulaması)
**Pages Analyzed:** 35 indexable URLs (full sitemap) + 4 extra 404 probes
**Language:** Turkish (`tr_TR`)

---

## Executive Summary

**Overall GEO Score: 45/100 (Poor)**

Malt Studio’s site is technically well-built for humans and Google: prerendered HTML, honest local copy, FAQ blocks, service/guide IA, `llms.txt` + Markdown twins, and LocalBusiness NAP in JSON-LD. Technical GEO is **85/100** — stronger than most local manufacturers.

The site is still largely invisible to the AI systems that cite and recommend businesses. Cloudflare’s managed robots block **GPTBot**, **ClaudeBot**, and **Google-Extended**. Live prerendered schema is a thin NAP stub. Brand authority is **7/100**: no YouTube, Reddit, Wikipedia, or GBP, and the name **Malt Studio** collides with Chicago’s Studio Malt, Paris’s Malt.com, and a Jakarta LinkedIn company (`linkedin.com/company/malt-studio` → maltstudio.com) that lists Özgür Nazım Gürbüz — so ChatGPT/Bing are more likely to describe the wrong entity.

Biggest strength: `llms.txt` quality (**87/100**) plus SSR. Most critical gap: Cloudflare AI crawl control + entity collision.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 54/100 | 25% | 13.5 |
| Brand Authority | 7/100 | 20% | 1.4 |
| Content E-E-A-T | 47/100 | 20% | 9.4 |
| Technical GEO | 85/100 | 15% | 12.8 |
| Schema & Structured Data | 48/100 | 10% | 4.8 |
| Platform Optimization | 31/100 | 10% | 3.1 |
| **Overall GEO Score** | | | **45/100** |

---

## Critical Issues (Fix Immediately)

### 1. Cloudflare blocks the AI crawlers that matter
`https://maltstudio.co/robots.txt` includes Cloudflare Managed Content:

| Crawler | Status | Impact |
|---|---|---|
| GPTBot | **BLOCKED** | ChatGPT training / browse corpus |
| ClaudeBot | **BLOCKED** | Claude search & URL analysis |
| Google-Extended | **BLOCKED** | Gemini / AI Overviews training signal |
| CCBot | BLOCKED | Common Crawl → many model datasets |
| Amazonbot | BLOCKED | Alexa / Amazon AI |
| Applebot-Extended | BLOCKED | Apple Intelligence |
| Bytespider | BLOCKED | ByteDance (optional to keep blocked) |
| PerplexityBot | Allowed by default | OK |
| OAI-SearchBot | Allowed by default | ChatGPT Search can still fetch |
| ChatGPT-User | Allowed by default | User-initiated visits work |

Content-Signal says `search=yes, ai-train=no, use=reference` — a reasonable legal stance — but `Disallow: /` on GPTBot/ClaudeBot overrides that for the bots people actually use.

**Fix:** In Cloudflare → AI Crawl Control / Bot Fight, allow **GPTBot**, **OAI-SearchBot**, **ChatGPT-User**, **ClaudeBot**, **PerplexityBot**, and **Google-Extended**. Keep `/admin/` and `/proje/` disallowed in the site’s own robots block. Bytespider can stay blocked.

### 2. Prerendered JSON-LD is a stub; the rich graph never ships
`content.json` already has `geoLatitude` / `geoLongitude`, `openingHours`, `priceRange`, Instagram. `index.html` builds Organization + LocalBusiness + WebSite + logo + OfferCatalog **in JavaScript**, then **skips it when `data-prerendered` is set**:

```js
if (!document.body.hasAttribute('data-prerendered')) {
  // full graph written here
}
```

Live homepage JSON-LD (what AI crawlers that do not run JS see):

- `@type`: LocalBusiness + ProfessionalService
- name, url, telephone, email, PostalAddress, areaServed (Tekirdağ, Süleymanpaşa), sameAs Instagram
- **Missing:** `logo`, `image`, `description`, `geo`, `openingHoursSpecification`, `hasMap`, `foundingDate`, `knowsAbout`, `WebSite`, `Organization`

Inner pages reference `https://maltstudio.co/#website` and `#business`, but the homepage graph never defines `#website`. That is a broken entity graph.

**Fix:** Bake the full graph into prerender (or stop gating it on `data-prerendered`). Align `@id` to one set (`#business` *or* `#localbusiness`, not both).

---

## High Priority Issues

### 3. No `FAQPage` schema on pages that already have FAQ copy
Homepage, every service page, atölye, and guides answer real questions (“Keşif ücretli mi?”, “Tabela ile ışıklı tabela farkı nedir?”). Zero `FAQPage` JSON-LD. Google AIO and Gemini extract these if marked up.

### 4. No llms.txt problem — but crawlers never get to use it
`llms.txt` (7.8 KB) and `llms-full.txt` (~174 KB) exist, are spec-shaped, and Markdown twins return `200` with `text/markdown` (verified: `/index.html.md`, `/hizmetler/tabela/index.html.md`). This is top-quartile for a local manufacturer. It does not help if GPTBot/ClaudeBot are disallowed.

### 5. Entity collision: “Malt Studio” is not a unique web entity
Search for the brand hits:

- This site (Tekirdağ tabela)
- Studio Malt (Chicago branding studio)
- Malt (Paris freelance marketplace, malt.com)
- **Jakarta LinkedIn** `linkedin.com/company/malt-studio` (maltstudio.com) — Advertising Services, Indonesia HQ, and lists Özgür Nazım Gürbüz as Head Graphic Designer, İstanbul. This is worse than absence: it actively trains the wrong HQ/country.

No Wikidata item, no Wikipedia article, no Tekirdağ LinkedIn company page (`content.json` `"linkedin": ""`), no YouTube channel, no Reddit threads, **no confirmed Google Business Profile**. Unbranded SERPs for “Tekirdağ tabela” / “Tekirdağ ışıklı tabela” are occupied by tekirdagreklam.com, sahibinden, and other firms — Malt ranks for branded queries only.

**Fix:** Claim GBP as “Malt Studio — Tekirdağ Tabela”; create a **new** LinkedIn Company Page (Süleymanpaşa, maltstudio.co) and do not attach to the Jakarta record; Wikidata item with official website + coordinates.

### 6. Missing trust pages
`/gizlilik/`, `/kvkk/`, `/hakkimizda/`, `/iletisim/`, `/privacy/` all **404**. Contact lives only at `/bolgeler/tekirdag/`. For Google E-E-A-T and local AI answers, a KVKK/privacy page and a short about/atölye story with a named person are expected.

### 7. Guides and sector pages have no structured data
All `/bilgi/*` and `/sektorler/*` pages: 0 JSON-LD. These are the most citable URLs (definitions, comparisons) and the least machine-labeled.

### 8. Case studies are too thin to cite
Six project pages: **130–136 words** each. Photos are real (strong Experience signal) but there is no problem → spec → material → result passage an AI can quote. No `CreativeWork`/`Article` schema.

---

## Medium Priority Issues

- **Citability length:** Scorer averages **25–32/100** on service/guide pages. Almost no 134–167 word self-contained passages. FAQ answers are 1–2 sentences (good for AIO, too short for ChatGPT-style citation).
- **Zero statistics:** No typical lead times, typical sizes, material lifetimes, or “kaç iş günü” ranges — even ranges would help. Site policy against fake metrics is correct; *real* workshop ranges are missing.
- **No comparison tables:** Işıklı vs ışıksız, pleksi vs paslanmaz are prose lists. AIO prefers HTML tables.
- **No visible dates** on guides (`datePublished` / `dateModified` not in schema or body). Sitemap `lastmod` is `2026-08-11` on many URLs; several hub/sector/guide URLs have **no `lastmod`**.
- **OG image alt is stale:** `Malt Studio — Marka Stratejisi ve Yaratıcı Ajans` while the live positioning is tabela/reklam üretimi.
- **`<br>` inside H2:** `Çalıştığımız<br>Sektörler` and `Bilgi<br>Merkezi` extract as `ÇalıştığımızSektörler` / `BilgiMerkezi` for tag-stripping crawlers.
- **Hub pages lack schema:** `/hizmetler/`, `/projeler/`, `/sektorler/`, `/bilgi/` have CollectionPage-worthy content and no JSON-LD.
- **sameAs is Instagram-only.** Add Google Maps, Wikidata (once created), Instagram, any Google Business URL.
- **No author / Person schema.** Fine for a workshop brand if Organization is complete; currently neither person nor full org ships.
- **Content-Signal `ai-train=no`:** Keep if you do not want training; it is not a substitute for allowing search bots.
- **Missing CSP** (other security headers are present). Low GEO impact, worth adding.

---

## Low Priority Issues

- Keywords meta still present (ignored by Google; harmless).
- HSTS is `max-age=31536000` without `includeSubDomains` / `preload`.
- WebFetch of `/sitemap.xml` returned 500 once; curl got **200** and 35 URLs. Treat as a flaky bot/UA issue, not a confirmed sitemap outage. Monitor.
- External links on homepage are WhatsApp only — no Google Maps `hasMap` in live schema despite atölye copy telling people to search Maps.
- `foundingDate` in CMS is empty.
- Copyright says 2025–2026; no “last updated” on rehber pages.

---

## Category Deep Dives

### AI Citability (54/100)

Script averages of 25–32 are a false floor (it skipped definitional one-liners). Expert rubric: answer quality 60, self-containment 54, structure 78, stats 16, uniqueness 45 → **54**. Coverage: ~20% of blocks score above 70; target is 60%+. Best pages: atölye NAP (~70), `/bilgi/tabela-cesitleri/` 58, `/hizmetler/tabela/` 56. Homepage 47 (card fragments). Project pages 22.

**What works**

- Question H2 on the homepage: “Tekirdağ’da hangi reklam ve tabela hizmetlerini veriyoruz?”
- FAQ blocks with direct answers on homepage, services, and atölye.
- Guide openings use definition patterns: “Kutu harf üç boyutlu cephe yazısıdır…”, “Totem … dikey sistemlerdir.”
- Numbered process (Keşif → Tasarım → Üretim → Montaj) is extractable as a HowTo-like list.
- Anti-hallucination policy is explicit (“uydurma şube/sertifika/metrik yazılmaz”) — good for accuracy, bad for hollow stats.

**What fails**

Automated passage scoring (20+ word blocks only):

| URL | Blocks | Avg score | Optimal 134–167w |
|---|---|---|---|
| / | 1 | 26 | 0 |
| /hizmetler/tabela/ | 6 | 31 | 0 |
| /hizmetler/isikli-tabela/ | 10 | 27 | 0 |
| /bilgi/tabela-cesitleri/ | 3 | 28 | 1 |
| /bilgi/isikli-mi-isiksiz-mi/ | 2 | 32 | 0 |
| /projeler/ofiso/ | 0 | 0 | 0 |

Rubric (expert, not only the script):

| Subscore | Score | Note |
|---|---|---|
| Answer block quality (30%) | 60 | FAQ + definitions exist; answers are too short |
| Self-containment (25%) | 54 | Short paras often name the subject |
| Structural readability (20%) | 78 | Lists/FAQ/H2s; no tables |
| Statistical density (15%) | 16 | Almost no numbers |
| Uniqueness (10%) | 45 | Real local process; repeated “Üretim, deneyim ve yerel uzmanlık” boilerplate on many URLs |

**Rewrite example** (from `/bilgi/tabela-cesitleri/` “Işıklı tabela” — currently one sentence)

*Current (low cite):* “Gece görünürlük gereken noktalarda LED’li sistemler kullanılır. Ayrı hizmet sayfası vardır.”

*Target (~150 words, self-contained):*

> Işıklı tabela, gece ve alacakaranlıkta da okunması gereken mağaza, tesis ve yol kenarı yazıları için LED aydınlatmalı bir tabela sistemidir. Tekirdağ’da Malt Studio ışıklı tabelayı ışıksız kompozit panelle karıştırmaz: ışıksız tabela gündüz okunur, ışıklı tabela ise kasa veya kutu harf içindeki LED ile gece de aynı mesajı taşır. Seçim üç soruya bağlıdır — tabela kim tarafından, hangi mesafeden ve hangi ışıkta okunacak? Cephede gece görünürlük yoksa ışıksız panel yeter; cadde, D-100 yaklaşımı veya vardiyalı tesis girişinde ışıklı sistem gerekir. Lightbox (iç mekân ışıklı kutu / SEG) ayrı bir üründür ve ışıklı cephe tabelasının yerine geçmez. Ölçü, montaj yüzeyi ve güç noktası keşifte not edilir; internette sabit fiyat listesi yoktur. Üretim ve montaj ayrıntısı Tekirdağ ışıklı tabela sayfasındadır: https://maltstudio.co/hizmetler/isikli-tabela/

Do this for: ışıklı vs ışıksız, kutu harf malzeme, totem vs cephe, fiyatı neler etkiler, and one expanded case study per vertical.

---

### Brand Authority (7/100)

| Platform | Presence | Score | Weight |
|---|---|---|---|
| YouTube | None found | 3/100 | 25% |
| Reddit | No threads | 2/100 | 25% |
| Wikipedia / Wikidata | None (en.wikipedia.org/wiki/Malt_Studio = 404) | 2/100 | 20% |
| LinkedIn | Jakarta `company/malt-studio` occupies the name; CMS empty | 6/100 | 15% |
| Directories / other | Armut.com listing; Instagram `@maltstudio.co` | 24/100 | 15% |

**Platform presence map**

| Signal | Status |
|---|---|
| Official website | Yes — maltstudio.co |
| Instagram | Yes — sameAs |
| Google Business Profile | Not confirmed from this audit (atölye asks users to search Maps; no `hasMap` URL in live schema) |
| YouTube | No |
| LinkedIn company | No (collision risk if created without “Tekirdağ / tabela” in the name line) |
| Wikipedia | No (notability likely insufficient — skip Wikipedia, **do** Wikidata) |
| Reddit / forum | None |
| Press / .edu | None found |
| Armut | Listed under Tekirdağ vinil germe tabela |

Name collision is the GEO-specific brand risk: unlinked mentions of “Malt Studio” in AI training data mostly belong to other firms. Disambiguate everywhere as **Malt Studio (Tekirdağ) — tabela ve reklam üretimi**, and put that string in schema `description`, GBP, Instagram bio, and Wikidata aliases.

---

### Content E-E-A-T (47/100)

| Dimension | Score | Evidence |
|---|---|---|
| Experience | 16/25 | Real project photos (OFİSO, Yamanlar, Anka, Köşem, Pembe Pasta, Okka Tarım); workshop-first copy; no measured outcomes on case pages |
| Expertise | 12/25 | Correct trade language (kompozit, SEG, OWV, kutu harf); no named fabricator, no author page, no methodology beyond the 4–6 step process |
| Authoritativeness | 6/25 | Almost no third-party citations; Armut listing only; entity drowned by larger “Malt” brands |
| Trustworthiness | 13/25 | HTTPS, NAP, phone, hours, honest “no fake reviews/metrics” policy; **no KVKK/privacy**; no reviews markup; contact URL is atölye not `/iletisim/` |

Repeated block “Üretim, deneyim ve yerel uzmanlık” on hizmet + bilgi + sektör pages is a topical-authority negative: AI sees the same paragraph, not new evidence.

**About gap:** There is no `/hakkimizda/`. The atölye page is the right canonical for NAP; it is not a people/credentials page.

---

### Technical GEO (85/100)

Crawlability 10/15 (AI bots blocked → 1/5 on that sub-check). Indexability 12/12. SSR 15/15. Security 9/10 (no CSP). CWV estimated 14/15. Page speed 10/15: homepage six JPEGs = **2.29 MB**; **WebP twins already 200** for all six (~1.56 MB) but `<img src>` still points at `.jpg`. `http://www` + missing slash can be a **3-hop** 301 chain. IndexNow key files 404. Sitemap curl 200 (WebFetch 500 was a UA flake). Markdown twins work; `Accept: text/markdown` on HTML URLs still returns HTML.

| Check | Result |
|---|---|
| HTTPS | Yes; HTTP → https://maltstudio.co/ 301 |
| www | https://www.maltstudio.co/ → apex 301 |
| Trailing slash | `/hizmetler` → `/hizmetler/` 301 |
| SSR / prerender | Yes — homepage ~73 KB HTML, 730 words in raw HTML, `has_ssr_content: true` |
| Canonical | Self-referencing on homepage |
| Viewport / mobile | Present |
| robots.txt | Valid; sitemap declared; `/admin/` and `/proje/` disallowed (correct) |
| XML sitemap | 35 URLs, `application/xml`, many `lastmod: 2026-08-11` |
| llms.txt | Present + full + .md twins |
| Security | HSTS, XFO, nosniff, Referrer-Policy, Permissions-Policy; **no CSP** |
| Host | Cloudflare + Netlify Edge |
| noindex | Not on public pages; `/admin/*` has X-Robots-Tag noindex |
| Core Web Vitals | Not lab-measured this run; HTML is prerendered (good for TTFB/crawl) |
| AI crawlers | **Fail** — see Critical #1 |

Crawl depth: all 35 sitemap URLs are linked from the homepage or one click off hubs. Good.

Markdown twins are a genuine GEO differentiator (few local TR sites have this).

---

### Schema & Structured Data (48/100)

**Found (live HTML JSON-LD)**

| Type | Where |
|---|---|
| LocalBusiness + ProfessionalService | Homepage (`#business`) |
| WebPage + BreadcrumbList | Service, project, atölye pages |
| Service | `/hizmetler/{slug}/` |
| *(none)* | `/bilgi/*`, `/sektorler/*`, hubs |

**Not found anywhere:** FAQPage, HowTo, Article/TechArticle, Review/AggregateRating, ImageObject, WebSite (in homepage graph), Organization as its own node, GeoCoordinates, OpeningHoursSpecification, CollectionPage.

**Validation notes**

- JSON is syntactically valid.
- Service `provider` points at `#business` (OK if homepage keeps that id).
- `isPartOf: #website` is a dangling reference.
- CMS has geo `40.9769375, 27.5041875` and hours Mon–Sat 09:00–19:00 — not in live JSON-LD.
- No `FAQPage` despite visible FAQ sections.

**Recommended homepage graph (ready to bake into prerender):**

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://maltstudio.co/#website",
      "url": "https://maltstudio.co/",
      "name": "Malt Studio",
      "inLanguage": "tr-TR",
      "publisher": { "@id": "https://maltstudio.co/#business" }
    },
    {
      "@type": ["LocalBusiness", "ProfessionalService"],
      "@id": "https://maltstudio.co/#business",
      "name": "Malt Studio",
      "description": "Tekirdağ Süleymanpaşa merkezli tabela üreticisi ve reklam uygulayıcısı. Tabela, ışıklı tabela, kutu harf, totem, cam ve araç giydirme — keşiften montaja.",
      "url": "https://maltstudio.co/",
      "telephone": "+905525826959",
      "email": "merhaba@maltstudio.co",
      "image": "https://maltstudio.co/images/og.jpg",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://maltstudio.co/#logo",
        "url": "https://maltstudio.co/images/icon-512.png"
      },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Yavuz Mahallesi, Ruşen Güneş Sokak, D Blok No:2",
        "postalCode": "59100",
        "addressLocality": "Süleymanpaşa",
        "addressRegion": "Tekirdağ",
        "addressCountry": "TR"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 40.9769375,
        "longitude": 27.5041875
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
        "opens": "09:00",
        "closes": "19:00"
      },
      "areaServed": [
        { "@type": "City", "name": "Tekirdağ" },
        { "@type": "AdministrativeArea", "name": "Süleymanpaşa" }
      ],
      "priceRange": "₺₺",
      "knowsAbout": ["Tabela", "Işıklı tabela", "Kutu harf", "Totem", "Araç giydirme", "Cam giydirme"],
      "sameAs": ["https://www.instagram.com/maltstudio.co/"]
    }
  ]
}
```

Add `FAQPage` on homepage and each service URL. Add `Article` + `dateModified` on `/bilgi/*`. Add `hasMap` once the Google Maps / GBP URL is confirmed.

---

### Platform Optimization (31/100)

| Platform | Score | Status | Why |
|---|---|---|---|
| Google AI Overviews | 50/100 | Moderate | Question H2s, FAQ, lists; **0 pts for top-10 rank** on unbranded “Tekirdağ tabela” |
| ChatGPT Web Search | 10/100 | Weak | No wiki/Wikidata; GPTBot blocked; Jakarta/Chicago name collision |
| Perplexity | 20/100 | Weak | Bot allowed; no Reddit/YouTube; short passages |
| Google Gemini | 28/100 | Weak | No GBP/Knowledge Panel; Google-Extended blocked; no YouTube |
| Bing Copilot | 45/100 | Moderate | Meta + exact-match titles strong; no IndexNow / Bing WMT / Places |

Google AIO is the only realistic near-term citation surface — and even that is capped until the shop ranks in the organic top 10 for “Tekirdağ tabela”. ChatGPT (10/100) will keep naming the wrong Malt until Wikidata + a Tekirdağ LinkedIn + GBP + unblocking GPTBot land.

---

## Quick Wins (Implement This Week)

1. **Cloudflare AI Crawl Control:** Allow GPTBot, ClaudeBot, Google-Extended, PerplexityBot. Highest GEO leverage on this site. Expected impact: ChatGPT/Claude/Gemini can actually retrieve the pages `llms.txt` already lists.
2. **Bake full JSON-LD in prerender** (geo, hours, logo, WebSite, description, knowsAbout). Stop skipping `buildStructuredData()` on prerendered HTML. Expected impact: Gemini/AIO entity grounding.
3. **Add FAQPage JSON-LD** to homepage + 10 hizmet pages (copy already exists). Expected impact: AIO extraction.
4. **Claim Google Business Profile** (and Bing Places) with the Süleymanpaşa NAP — Gemini/AIO local have nothing to quote today.
5. **Point homepage `<img>` at existing WebP files** (six JPEGs = 2.29 MB; WebP twins already 200).
6. **Fix OG/Twitter image alt** to tabela positioning, not “Yaratıcı Ajans”.
7. **Replace H2 `<br>` with a space or CSS break** so crawlers read “Çalıştığımız Sektörler” and “Bilgi Merkezi”.
8. **Publish `/kvkk/` (or `/gizlilik/`)** with a footer link. Expected impact: Trust / E-E-A-T, not citations.
9. **One HTML comparison table** on `/bilgi/isikli-mi-isiksiz-mi/` (özellik / ışıklı / ışıksız).

---

## 30-Day Action Plan

### Week 1: Let AI in + machine-readable entity
- [ ] Cloudflare: allow GPTBot, ClaudeBot, Google-Extended, PerplexityBot
- [ ] Prerender full LocalBusiness graph (geo, hours, WebSite `@id`, logo)
- [ ] FAQPage on homepage + core hizmet URLs
- [ ] Confirm / complete Google Business Profile; put Maps URL in `hasMap` + `sameAs`
- [ ] Isolate LinkedIn: new Tekirdağ company page (maltstudio.co) — do not use Jakarta `company/malt-studio`
- [ ] Switch homepage project `<img>` to existing WebP
- [ ] Fix OG alt + H2 `<br>` concatenation

### Week 2: Citability of pages you already have
- [ ] Expand ışıklı vs ışıksız, tabela çeşitleri, kutu harf malzemeler, tabela fiyatı to 1–2 self-contained 120–160 word answer blocks each
- [ ] Add one comparison `<table>` per comparison guide
- [ ] `Article` schema + visible “Güncelleme: YYYY-MM-DD” on all `/bilgi/*`
- [ ] Align sitemap `lastmod` on bilgi/sektör URLs

### Week 3: Proof and disambiguation
- [ ] Expand 3 project pages to ~400–600 words (yüzey, malzeme, gece/gündüz ihtiyacı, montaj notu) — still no fake KPIs
- [ ] Create a Wikidata item: Malt Studio (Tekirdağ), official website, coordinates, instance of signage manufacturer
- [ ] LinkedIn company page titled to include Tekirdağ / tabela
- [ ] Short atölye/about block with a real person name + role (Person schema)

### Week 4: Platforms that AIO/Gemini actually cite
- [ ] 3 YouTube shorts: keşif, kutu harf vs ışıklı, totem montaj — descriptions with full URLs + transcript
- [ ] KVKK page + footer
- [ ] IndexNow ping on publish (helps Bing/Copilot)
- [ ] Re-run this audit; target **60+** once crawlers are allowed and schema is baked

---

## Appendix: Pages Analyzed

| URL | Title | GEO Issues |
|---|---|---|
| https://maltstudio.co/ | Tekirdağ Reklam Ajansı ve Tabela \| Malt Studio | Thin live schema; FAQ untyped; H2 br-concat |
| https://maltstudio.co/hizmetler/ | Hizmetler hub | No schema |
| https://maltstudio.co/bolgeler/tekirdag/ | Atölye ve iletişim | NAP in body; hours not in JSON-LD; no LocalBusiness on this URL |
| https://maltstudio.co/projeler/ | Projeler hub | No schema |
| https://maltstudio.co/sektorler/ | Sektörler hub | No schema |
| https://maltstudio.co/bilgi/ | Bilgi hub | No schema |
| https://maltstudio.co/hizmetler/tabela/ | Tabela imalatı | Service+Breadcrumb; no FAQPage; citability ~31 |
| https://maltstudio.co/hizmetler/isikli-tabela/ | Işıklı tabela | Same pattern |
| https://maltstudio.co/hizmetler/kutu-harf/ | Kutu harf | Same pattern |
| https://maltstudio.co/hizmetler/totem/ | Totem | Same pattern |
| https://maltstudio.co/hizmetler/arac-giydirme/ | Araç giydirme | Same pattern |
| https://maltstudio.co/hizmetler/cam-giydirme/ | Cam giydirme | Same pattern |
| https://maltstudio.co/hizmetler/lightbox/ | Lightbox | Same pattern |
| https://maltstudio.co/hizmetler/display-pos/ | Display & POS | Same pattern |
| https://maltstudio.co/hizmetler/ofis-branding/ | Ofis branding | Same pattern |
| https://maltstudio.co/hizmetler/is-guvenligi-tabelalari/ | İSG tabelaları | Same pattern |
| https://maltstudio.co/projeler/ofiso/ | OFİSO | Thin (~132 words) |
| https://maltstudio.co/projeler/yamanlar-ekspertiz/ | Yamanlar Ekspertiz | Thin |
| https://maltstudio.co/projeler/anka/ | Anka Anaokulu | Thin |
| https://maltstudio.co/projeler/kosem-doner/ | Köşem Döner | Thin |
| https://maltstudio.co/projeler/pembe-pasta-evi/ | Pembe Pasta Evi | Thin |
| https://maltstudio.co/projeler/okka-tarim/ | Okka Tarım | Thin |
| https://maltstudio.co/sektorler/fabrika-osb/ | Fabrika & OSB | No schema; boilerplate E-E-A-T block |
| https://maltstudio.co/sektorler/restoran-cafe/ | Restoran & Cafe | No schema |
| https://maltstudio.co/sektorler/saglik/ | Sağlık | No schema |
| https://maltstudio.co/sektorler/plaza-ofis/ | Plaza & Ofis | No schema |
| https://maltstudio.co/sektorler/insaat-santiye/ | İnşaat & Şantiye | No schema |
| https://maltstudio.co/sektorler/perakende/ | Perakende | No schema |
| https://maltstudio.co/bilgi/tabela-cesitleri/ | Tabela çeşitleri | Best definition page; no Article/FAQ schema |
| https://maltstudio.co/bilgi/isikli-mi-isiksiz-mi/ | Işıklı mı ışıksız mı | No table |
| https://maltstudio.co/bilgi/kutu-harf-malzemeler/ | Kutu harf malzemeler | No schema |
| https://maltstudio.co/bilgi/one-way-vision-nedir/ | One way vision | No schema |
| https://maltstudio.co/bilgi/arac-giydirme-rehberi/ | Araç giydirme rehberi | No schema |
| https://maltstudio.co/bilgi/tabela-fiyati/ | Tabela fiyatı | No schema; no numeric ranges |
| https://maltstudio.co/bilgi/totem-secim-rehberi/ | Totem seçim | No schema |
| https://maltstudio.co/gizlilik/ | — | **404** |
| https://maltstudio.co/kvkk/ | — | **404** |
| https://maltstudio.co/hakkimizda/ | — | **404** |
| https://maltstudio.co/iletisim/ | — | **404** (canonical contact is `/bolgeler/tekirdag/`) |

**Fetch notes:** All 35 sitemap URLs returned **200**. `llms.txt` / `llms-full.txt` 200. Markdown twins 200. Sitemap XML 200 via curl (35 loc). Robots.txt 200. Extra legal/about paths 404.

**Scoring formula:**  
`GEO = Citability×0.25 + Brand×0.20 + EEAT×0.20 + Technical×0.15 + Schema×0.10 + Platform×0.10`
