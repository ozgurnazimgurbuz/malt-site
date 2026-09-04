# Cloudflare Pages — adım adım kurulum

**Güncel değil.** Site Amazon’da; Netlify kullanılmıyor. Bu dosya eski geçiş notudur.

Bu rehber yazılım bilmeden takip edilebilir. Kod tarafı repoda hazır; sen sadece Cloudflare panelinde tıklayacaksın.

## Senin yapacağın (Adım 1 — şimdi)

1. Tarayıcıda aç: **https://dash.cloudflare.com/sign-up** (hesabın varsa giriş yap).
2. Sol menüden **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
3. **GitHub** ile bağlan; `ozgurnazimgurbuz/malt-site` reposunu seç.
4. Ayarları **tam olarak** şöyle gir:

   | Alan | Değer |
   | --- | --- |
   | Production branch | `main` |
   | Framework preset | **None** |
   | Build command | `pip install -r requirements.txt && python3 scripts/optimize_uploads.py && python3 scripts/build_production.py && python3 scripts/build_project_tracking.py && python3 scripts/scrub_customer_copy.py && python3 scripts/prerender.py && python3 scripts/build_llms.py && python3 scripts/minify_assets.py` |
   | Build output directory | `.` (nokta — kök dizin) |

5. **Environment variables** (Build) ekle:

   | Name | Value |
   | --- | --- |
   | `PYTHON_VERSION` | `3.11` |

6. **Save and Deploy** — ilk build 2–4 dakika sürebilir.
7. Build bitince sana `https://malt-site-xxxx.pages.dev` gibi bir adres verir. Aç; site görünüyorsa **bana “build oldu” yaz**, DNS adımına geçeriz.

## Sonraki adımlar (birlikte)

- **Adım 2:** `maltstudio.co` domain’ini Cloudflare Pages projesine bağlamak
- **Adım 3:** DNS’i Netlify’dan Cloudflare’e taşımak (nameserver veya kayıt güncelleme)
- **Adım 4:** Canlıda kontrol (Mantra tracking `track18`, redirect’ler)
- **Adım 5:** Netlify’ı kapatmak

## İçerik güncelleme (panel yok)

Değişiklikler Cursor + GitHub üzerinden:

1. Dosyayı düzenle (ör. `content.json`, proje JSON’ları)
2. Commit + push → Cloudflare otomatik yeniden build eder

## Sorun çıkarsa

Cloudflare → Pages → projen → **Deployments** → kırmızı satıra tıkla → **Build log** ekran görüntüsünü paylaş.
