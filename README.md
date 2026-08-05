# Malt Studio

Tekirdağ merkezli marka stratejisi ve yaratıcı ajans için tek sayfalık tanıtım sitesi.
Build adımı yoktur; statik dosyalar doğrudan yayımlanır. İçerik Decap CMS ile yönetilir.

Üretim adresi: https://maltstudio.co

## Dosya yapısı

| Yol | Görev |
| --- | --- |
| `index.html` | Tüm işaretleme, stil ve `content.json` okuyan istemci tarafı mantık |
| `content.json` | CMS tarafından yazılan tek içerik kaynağı (düz JSON) |
| `admin/index.html` | Decap CMS giriş noktası (sürüm sabitlenmiş) |
| `admin/config.yml` | CMS alan tanımları, Git Gateway ayarı |
| `images/` | Statik görseller ve uygulama ikonları |
| `images/uploads/` | CMS üzerinden yüklenen medya (ilk yüklemede oluşur) |
| `manifest.json` | Web app manifest |
| `robots.txt`, `sitemap.xml` | Arama motoru yönlendirmesi |
| `netlify.toml` | Yayın ayarları, güvenlik başlıkları, önbellek kuralları |

## Yerel geliştirme

```bash
python3 -m http.server 8800
```

`http://localhost:8800` adresini açın. Yönetim paneli (`/admin/`) yerelde giriş yapamaz;
Netlify Identity yalnızca yayımlanmış ortamda çalışır.

## Yayın

Netlify, `main` dalını izler ve depo kökünü yayımlar. Build komutu yoktur.

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
- **og:image** yalnızca `siteUrl` ve `seoOgImage` birlikte doluysa üretilir.
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
