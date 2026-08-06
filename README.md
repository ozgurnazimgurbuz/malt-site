# Malt Studio

Tekirdağ merkezli marka stratejisi ve yaratıcı ajans için tek sayfalık tanıtım sitesi.
Her Netlify deploy’unda `scripts/prerender.py`, `content.json` içeriğini `index.html` içine gömer.
Böylece kritik metin View Source’da JS olmadan görünür. Decap CMS yalnızca `content.json` yazar.

Üretim adresi: https://maltstudio.co

## Dosya yapısı

| Yol | Görev |
| --- | --- |
| `index.html` | İşaretleme, stil; kritik içerik prerender ile gömülür |
| `content.json` | CMS tarafından yazılan tek içerik kaynağı (düz JSON) |
| `scripts/prerender.py` | `content.json` → `index.html` (Netlify build) |
| `admin/index.html` | Decap CMS giriş noktası (sürüm sabitlenmiş) |
| `admin/config.yml` | CMS alan tanımları, Git Gateway ayarı |
| `images/` | Statik görseller ve uygulama ikonları |
| `images/uploads/` | CMS üzerinden yüklenen medya (ilk yüklemede oluşur) |
| `manifest.json` | Web app manifest |
| `robots.txt`, `sitemap.xml` | Arama motoru yönlendirmesi |
| `netlify.toml` | Build, güvenlik başlıkları, önbellek |

## Yerel geliştirme

```bash
python3 scripts/prerender.py
python3 -m http.server 8800
```

`http://localhost:8800` adresini açın. Yönetim paneli (`/admin/`) yerelde giriş yapamaz;
Netlify Identity yalnızca yayımlanmış ortamda çalışır.

## Yayın

Netlify, `main` dalını izler. Build komutu: `python3 scripts/prerender.py` — ardından kök dizin yayımlanır.

CMS'in çalışması için Netlify tarafında şunlar açık olmalıdır:

1. **Identity** etkin
2. **Registration: Invite only**
3. **Services → Git Gateway** etkin

Kullanıcılar Identity üzerinden davet edilir; davet bağlantısı `/admin/` adresine yönlenir.

## İçerik yönetimi

Tüm alanlar `admin/config.yml` içinde tanımlıdır. Boş bırakılan alanlar sitedeki
mevcut değeri ezmez:

- **Logo** boşsa gömülü SVG logo gösterilir.
- **Portfolyo görseli** boşsa mevcut gradyan yer tutucu gösterilir.
- **SEO alanları** boşsa `index.html` içindeki statik değerler korunur.
- **og:image** `siteUrl` + `seoOgImage` ile mutlak adres üretir; varsayılan marka görseli `/images/og.jpg` (1200×630).
- **google-site-verification** yalnızca alan doluysa yazılır.

Analitik alanları (`googleAnalyticsId`, `googleTagManagerId`, `facebookPixelId`)
yalnızca değer saklar; hiçbir izleme betiği yüklenmez.

## İkonlar

`images/icon-192.png` ve `images/icon-512.png`, `images/icon-source.svg` dosyasından
üretilir. Kaynak SVG orijinal Malt Studio wordmark path verisini birebir içerir.
Yeniden üretmek için:

```bash
qlmanage -t -s 512 -o images images/icon-source.svg && mv images/icon-source.svg.png images/icon-512.png
qlmanage -t -s 192 -o images images/icon-source.svg && mv images/icon-source.svg.png images/icon-192.png
```
