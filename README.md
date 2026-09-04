# Malt Studio

Tekirdağ merkezli marka stratejisi ve yaratıcı ajans için tek sayfalık tanıtım sitesi.
Kaynak `main` dalıdır; yayın Amazon üzerinde. Build pipeline (`scripts/prerender.py`) `content.json` içeriğini `index.html` içine gömer.
Böylece kritik metin View Source’da JS olmadan görünür. İçerik `content.json` ve proje JSON dosyalarından gelir (Cursor üzerinden düzenlenir).

Üretim adresi: https://maltstudio.co

## Dosya yapısı

| Yol | Görev |
| --- | --- |
| `index.html` | İşaretleme, stil; kritik içerik prerender ile gömülür |
| `content.json` | CMS tarafından yazılan tek içerik kaynağı (düz JSON) |
| `scripts/prerender.py` | `content.json` → `index.html` (deploy build) |
| `_redirects`, `_headers` | Yönlendirme ve önbellek kuralları (eski Pages/Netlify biçimi; origin’de karşılığı yoksa uygulanmaz) |
| `DEPLOY-CLOUDFLARE.md` | Eski Cloudflare kurulum notu; aktif hosting Amazon |
| `images/` | Statik görseller ve uygulama ikonları |
| `images/uploads/` | CMS üzerinden yüklenen medya (ilk yüklemede oluşur) |
| `manifest.json` | Web app manifest |
| `robots.txt`, `sitemap.xml` | Arama motoru yönlendirmesi |
| `netlify.toml` | Eski Netlify ayarları (referans; aktif hosting Amazon) |

## Yerel geliştirme

```bash
python3 scripts/prerender.py
python3 -m http.server 8800
```

`http://localhost:8800` adresini açın.

## Yayın

Hosting Amazon. Kaynak dal `main`. `DEPLOY-CLOUDFLARE.md` eski kurulum notudur.

Yerel / CI build komutu:

```bash
pip install -r requirements.txt && python3 scripts/optimize_uploads.py && python3 scripts/build_production.py && python3 scripts/build_project_tracking.py && python3 scripts/scrub_customer_copy.py && python3 scripts/prerender.py && python3 scripts/build_llms.py && python3 scripts/minify_assets.py
```

## İçerik yönetimi

Ana içerik `content.json`; proje takip sayfaları `content/proje/*.json`. Boş bırakılan alanlar sitedeki
mevcut değeri ezmez:

- **Logo** boşsa gömülü SVG logo gösterilir.
- **Portfolyo görseli** boşsa mevcut gradyan yer tutucu gösterilir.
- **SEO alanları** boşsa `index.html` içindeki statik değerler korunur.
- **og:image** `siteUrl` + `seoOgImage` ile mutlak adres üretir; varsayılan marka görseli `/images/og.jpg` (1200×630).
- **google-site-verification** yalnızca alan doluysa yazılır.

`googleAnalyticsId` (GA4 Measurement ID, örn. `G-…`) doluysa `scripts/lib_site.py`
ve `scripts/prerender.py` tüm public sayfa `<head>` içine deferred gtag yükler
(`requestIdleCallback` / `load`). `googleTagManagerId` ve `facebookPixelId`
yalnızca CMS’de saklanır; henüz script enjekte edilmez.

## İkonlar

`images/icon-192.png` ve `images/icon-512.png`, `images/icon-source.svg` dosyasından
üretilir. Kaynak SVG orijinal Malt Studio wordmark path verisini birebir içerir.
Yeniden üretmek için:

```bash
qlmanage -t -s 512 -o images images/icon-source.svg && mv images/icon-source.svg.png images/icon-512.png
qlmanage -t -s 192 -o images images/icon-source.svg && mv images/icon-source.svg.png images/icon-192.png
```
