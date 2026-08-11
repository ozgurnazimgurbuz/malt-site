#!/usr/bin/env python3
"""Wave A2: Lightbox, Display POS, Ofis Branding, İş Güvenliği Tabelaları."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://maltstudio.co"
PHONE_DISPLAY = "0552 582 69 59"
PHONE_TEL = "+905525826959"
WA = "905525826959"
EMAIL = "merhaba@maltstudio.co"

A0_SERVICES = {
    "tabela": "Tabela",
    "isikli-tabela": "Işıklı Tabela",
    "kutu-harf": "Kutu Harf",
    "totem": "Totem",
    "arac-giydirme": "Araç Giydirme",
    "cam-giydirme": "Cam Giydirme",
}

A2_SERVICES = [
    {
        "slug": "lightbox",
        "name": "Lightbox",
        "pk": "lightbox",
        "title": "Lightbox | Işıklı Kutu ve Backlit Frame Sistemleri",
        "description": "Lightbox, ışıklı kutu, SEG ve backlit fabric frame üretimi. Malt Studio.",
        "lede": "Mağaza, AVM ve ofislerde ince kasa ışıklı kutu / lightbox sistemleri.",
        "overview": (
            "Lightbox (ışıklı kutu / light box); kumaş veya sert yüzeyin arkadan aydınlatıldığı "
            "çerçeve sistemidir. Bu sayfa lightbox / ışıklı kutu / SEG / backlit frame "
            "birincil sahibidir. Klasik cephe ‘ışıklı tabela’ niyeti "
            "/hizmetler/isikli-tabela/ sayfasındadır — karıştırılmaz."
        ),
        "benefits": [
            "Homojen ışık dağılımı",
            "İnce kasa / premium retail görünüm",
            "SEG / tekstil frame ile hızlı görsel değişimi",
            "AVM ve vitrin vitrin içi uygulamalar",
        ],
        "apps": [
            "Mağaza ve showroom duvarları",
            "AVM mağaza içi / vitrin arkası",
            "Eczane ve klinik bekleme alanları",
            "Ofis ve resepsiyon marka duvarları",
        ],
        "materials": "Alüminyum kasa, LED edge/backlight, backlit fabric, SEG silikon kenar, akrilik yüz seçenekleri.",
        "process": "Ölçü → kasa tipi seçimi → baskı / kumaş → kasa montajı → saha kurulum.",
        "pricing": "Ölçü, kasa tipi (klik/SEG), LED tipi ve baskı yüzeyi fiyatı belirler.",
        "timeline": "Standart ölçülerde hızlı; özel kasa ve saha koşullarında süre uzar.",
        "faqs": [
            ("Lightbox ile ışıklı tabela aynı mı?", "Hayır. Işıklı tabela genelde cephe tabela sistemidir. Lightbox çerçeve/ışıklı kutu sistemidir."),
            ("SEG nedir?", "Silicone Edge Graphic — kumaşın kasaya silikon kenarla gerildiği sistem."),
            ("Tekirdağ’da var mı?", "Evet. Keşif Tekirdağ üssünden planlanır. Ayrı S×C sayfası bu dalgada yok."),
        ],
        "related": ["isikli-tabela", "display-pos", "ofis-branding", "cam-giydirme"],
        "disambiguation": "PK lock: led tabela / ışıklı tabela → /hizmetler/isikli-tabela/. Bu sayfa yalnızca lightbox ailesi.",
    },
    {
        "slug": "display-pos",
        "name": "Display & POS",
        "pk": "roll-up",
        "title": "Roll-Up, X-Banner ve POS Display Sistemleri",
        "description": "Roll-up, X-banner, beach flag, broşür standı ve POS display üretimi. Malt Studio.",
        "lede": "Taşınabilir display ve POS sistemleri: roll-up, X-banner, bayrak ve teşhir.",
        "overview": (
            "Display & POS; roll-up, X-banner / örümcek, beach/Y flag, broşür standı ve teşhir "
            "ünitelerini kapsar. Bu sayfa taşınabilir display donanımının sahibidir. "
            "Fuar standı / backdrop ortamı sonraki ‘fuar-stand’ dalgasına aittir — "
            "roll-up PK’si burada kalır."
        ),
        "benefits": [
            "Hızlı kurulum / söküm",
            "Kampanya ve etkinlik esnekliği",
            "Mağaza içi POS görünürlük",
            "Baskı + donanım tek elden",
        ],
        "apps": [
            "Mağaza ve showroom içi",
            "Fuar ve etkinlik (tekil display)",
            "Lansman ve bayilik toplantıları",
            "Geçici yön / kampanya noktaları",
        ],
        "materials": "Roll-up kasalar, X-banner iskeletleri, beach flag direkleri, dekota/forex tamamlayıcılar, vinil/textile baskı.",
        "process": "İhtiyaç → boyut → baskı → donanım montajı / teslim.",
        "pricing": "Donanım tipi, baskı ölçüsü ve adet fiyatı belirler.",
        "timeline": "Çoğu display işi kısa üretim döngüsündedir.",
        "faqs": [
            ("Roll-up ile X-banner farkı?", "Roll-up kasalı ve daha premium; X-banner daha ekonomik örümcek ayaklıdır."),
            ("Fuar standı da burada mı?", "Tekil display evet. Tam stand / backdrop ortamı ayrı fuar hizmetine aittir."),
            ("Indoor totem display?", "Taşınabilir bilgi totemleri bu ailede; dış mekân yol totemi /hizmetler/totem/ altındadır."),
        ],
        "related": ["lightbox", "tabela", "cam-giydirme", "ofis-branding"],
        "disambiguation": "PK lock: roll-up / x-banner / beach flag → bu sayfa. Outdoor totem → /hizmetler/totem/.",
    },
    {
        "slug": "ofis-branding",
        "name": "Ofis Branding",
        "pk": "ofis branding",
        "title": "Ofis Branding | Resepsiyon, Lobi ve Kurumsal Ofis Grafikleri",
        "description": "Ofis branding, resepsiyon tabela, lobi logo duvarı ve kurumsal ofis grafikleri. Malt Studio.",
        "lede": "Resepsiyon, lobi ve toplantı alanlarında kurumsal kimliğin mekâna uygulanması.",
        "overview": (
            "Ofis branding; resepsiyon yazısı, lobi logo duvarı, toplantı odası grafikleri ve "
            "kurumsal ofis görünürlüğünü paketler. Bu sayfa workplace kimlik paketinin sahibidir. "
            "Genel duvar/zemin giydirme (her mekân) sonraki iç-mekan-giydirme sayfasına aittir. "
            "Cam folyo malzemesi /hizmetler/cam-giydirme/ ile bağlanır; ofis paketi burada satılır."
        ),
        "benefits": [
            "Tutarlı kurumsal ilk izlenim",
            "Resepsiyon ve lobi odaklı paket",
            "Cam + duvar + yazı kombinasyonu",
            "Plaza / ofis teslimatlarına uyum",
        ],
        "apps": [
            "Plaza ve iş merkezi ofisleri",
            "Resepsiyon / lobi",
            "Toplantı odaları",
            "Kurumsal kat kimliği",
        ],
        "materials": "Kutu harf / logo duvarı, cam folyo (gizlilik/baskı), duvar grafikleri, oda/kapı isimlikleri (yönlendirme ile birlikte).",
        "process": "Keşif → marka dosyası → uygulama planı → üretim → mesaiye duyarlı montaj.",
        "pricing": "Alan m², harf/logo tipi, cam folyo oranı ve kat erişimi fiyatı belirler.",
        "timeline": "Ofis kesintisini azaltmak için genelde planlı kısa pencerelerde uygulanır.",
        "faqs": [
            ("Kapı isimliği de dahil mi?", "Pakete eklenebilir. Saf wayfinding sistemi yönlendirme hizmetine aittir (sonraki dalga)."),
            ("Cam giydirme ayrı mı?", "Cam uygulama cam giydirme uzmanlığındadır; ofis paketi burada yönetilir."),
            ("İç mekan giydirme ile farkı?", "Ofis branding workplace kimlik paketidir; genel duvar/zemin her mekân için ayrı aile."),
        ],
        "related": ["kutu-harf", "cam-giydirme", "lightbox", "tabela"],
        "disambiguation": "PK lock: ofis branding / resepsiyon / lobi → bu sayfa. Cam yazısı tekil → cam-giydirme.",
    },
    {
        "slug": "is-guvenligi-tabelalari",
        "name": "İş Güvenliği Tabelaları",
        "pk": "iş güvenliği tabelaları",
        "title": "İş Güvenliği Tabelaları | Uyarı, Yangın Çıkışı, İSG Levhaları",
        "description": "İş güvenliği tabelaları, uyarı levhaları, yangın çıkışı ve acil durum işaretleri. Malt Studio.",
        "lede": "Fabrika, depo ve şantiyeler için İSG uyarı, zorunlu ve acil çıkış tabelaları.",
        "overview": (
            "İş güvenliği tabelaları; uyarı, yasak, zorunlu işaretler, yangın/acil çıkış ve "
            "toplanma alanı levhalarını kapsar. Bu sayfa statutory/uyarı setlerinin sahibidir. "
            "Yön bulma (oda, kat, directory) wayfinding ailesine aittir — karıştırılmaz. "
            "İçerik üretim/tedarik odaklıdır; sertifikasyon otoritesi iddiası yoktur."
        ),
        "benefits": [
            "Standart işaret setleri",
            "OSB / fabrika / depo uyumu",
            "Dayanıklı dış/iç malzeme seçenekleri",
            "Toplu saha etiketleme",
        ],
        "apps": [
            "Fabrika ve OSB tesisleri",
            "Depo ve lojistik alanları",
            "Şantiye çevreleri",
            "Ortak alan acil yön işaretleri",
        ],
        "materials": "Kompozit/forex levhalar, reflektif folyo (ihtiyaca göre), fotolüminesans yalnızca sunuluyorsa.",
        "process": "İhtiyaç listesi → işaret seti → baskı/kesim → saha montaj planı.",
        "pricing": "Adet, ölçü, malzeme ve montaj sahası fiyatı belirler.",
        "timeline": "Standart setlerde hızlı üretim; büyük tesislerde planlı montaj.",
        "faqs": [
            ("Yangın çıkışı tabela burada mı?", "Evet. Acil/yangın çıkış işaretleri bu ailededir."),
            ("Yönlendirme tabelası aynı mı?", "Hayır. Oda/kat/directory wayfinding ayrıdır."),
            ("ISO belgesi veriyor musunuz?", "Tabela üretiriz; belgelendirme kuruluşu değiliz."),
        ],
        "related": ["tabela", "totem", "display-pos", "ofis-branding"],
        "disambiguation": "PK lock: İSG / uyarı / yangın çıkışı → bu sayfa. Wayfinding → yönlendirme (henüz A2 dışı).",
    },
]


def wa(msg: str) -> str:
    return f"https://wa.me/{WA}?text={quote(msg)}"


def logo() -> str:
    return (
        '<img class="logo-mark" src="/images/logo.svg" width="120" height="19" '
        'alt="Malt Studio" onerror="this.style.display=\'none\'">'
    )


def head(title: str, description: str, canonical: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Malt Studio">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="tr_TR">
<meta property="og:image" content="{SITE}/images/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE}/images/og.jpg">
<link rel="icon" type="image/png" href="/images/icon-192.png">
<link rel="manifest" href="/manifest.json">
<link rel="preload" href="/assets/fonts/big-shoulders-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/big-shoulders-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts.css">
<link rel="stylesheet" href="/assets/site.css">
</head>
"""


def header() -> str:
    return f"""<header>
  <a href="/" aria-label="Malt Studio ana sayfa">{logo()}</a>
  <nav>
    <a href="/hizmetler/">Hizmetler</a>
    <a href="/projeler/">Projeler</a>
    <a href="/sektorler/">Sektörler</a>
    <a href="/bilgi/">Bilgi</a>
    <a href="/bolgeler/tekirdag/">Tekirdağ</a>
  </nav>
</header>
"""


def footer() -> str:
    a0 = "\n".join(
        f'<li><a href="/hizmetler/{s}/">{n}</a></li>' for s, n in A0_SERVICES.items()
    )
    a2 = "\n".join(
        f'<li><a href="/hizmetler/{s["slug"]}/">{s["name"]}</a></li>' for s in A2_SERVICES
    )
    return f"""<footer>
  <div class="wrap">
    <div class="footer-top">
      <div>
        <div class="footer-logo">{logo()}</div>
        <p style="font-size:14px;line-height:1.6;color:rgba(241,238,231,0.65);max-width:280px;">
          Wave A2: lightbox, display/POS, ofis branding ve iş güvenliği tabelaları.
        </p>
      </div>
      <div>
        <h4>A0 Hizmetler</h4>
        <ul>{a0}</ul>
      </div>
      <div>
        <h4>A2 Hizmetler</h4>
        <ul>{a2}</ul>
      </div>
      <div>
        <h4>İletişim</h4>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="/bolgeler/tekirdag/">Tekirdağ</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2025–2026 Malt Studio</span>
      <span>Wave A2</span>
    </div>
  </div>
</footer>
<a class="whatsapp-btn" href="{wa("Merhaba, A2 hizmetleriniz hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
"""


def crumbs(*parts: tuple[str, str | None]) -> str:
    bits = []
    for label, href in parts:
        if href:
            bits.append(f'<a href="{href}">{label}</a><span>/</span>')
        else:
            bits.append(f"<span>{label}</span>")
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{"".join(bits)}</nav>'


def faq_html(faqs: list[tuple[str, str]]) -> str:
    return "\n".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def resolve_name(slug: str) -> str:
    for s in A2_SERVICES:
        if s["slug"] == slug:
            return s["name"]
    return A0_SERVICES.get(slug, slug)


def related_cards(slugs: list[str]) -> str:
    cards = []
    for slug in slugs:
        cards.append(
            f'<a class="card" href="/hizmetler/{slug}/"><h3>{resolve_name(slug)}</h3>'
            f"<p>İlgili hizmet — ayrı PK owner.</p>"
            f'<span class="meta">Hizmet</span></a>'
        )
    return "\n".join(cards)


def build_service(s: dict) -> None:
    canonical = f"{SITE}/hizmetler/{s['slug']}/"
    benefits = "".join(f"<li>{b}</li>" for b in s["benefits"])
    apps = "".join(f"<li>{a}</li>" for a in s["apps"])
    w = wa(f"Merhaba, {s['name']} hizmeti hakkında bilgi almak istiyorum.")
    html = f"""{head(s["title"], s["description"], canonical)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Hizmetler", "/hizmetler/"), (s["name"], None))}
    <div class="eyebrow">Wave A2 · Service · Non-geo owner</div>
    <h1>{s["name"]}</h1>
    <p class="lede">{s["lede"]}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{w}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_DISPLAY}</a>
      <a class="btn btn-ghost" href="/bolgeler/tekirdag/">Tekirdağ</a>
    </div>
    <div class="trust-strip">
      <span><strong>Owner PK:</strong> {s["pk"]}</span>
      <span><strong>S×C:</strong> bu dalgada yok</span>
      <span><strong>Wave:</strong> A2</span>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    <div class="content-block">
      <h2>Bu hizmet nedir?</h2>
      <p>{s["overview"]}</p>
      <p class="note">{s["disambiguation"]}</p>
    </div>
    <div class="content-block">
      <h2>Kimler için uygun?</h2>
      <ul>{apps}</ul>
    </div>
    <div class="content-block">
      <h2>Avantajlar</h2>
      <ul>{benefits}</ul>
    </div>
    <div class="content-block">
      <h2>Malzeme ve seçenekler</h2>
      <p>{s["materials"]}</p>
    </div>
    <div class="content-block">
      <h2>Üretim süreci</h2>
      <p>{s["process"]}</p>
    </div>
    <div class="content-block">
      <h2>Fiyatı neler etkiler?</h2>
      <p>{s["pricing"]}</p>
    </div>
    <div class="content-block">
      <h2>Süre</h2>
      <p>{s["timeline"]}</p>
    </div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Yerel ve kanıt bağlantıları</h2>
    <p class="intro">A2 için ayrı Service×City URL’si açılmadı (doorway riski yok).</p>
    <div class="card-grid">
      <a class="card" href="/bolgeler/tekirdag/"><h3>Tekirdağ</h3><p>Şehir hub.</p><span class="meta">City</span></a>
      <a class="card" href="/projeler/"><h3>Projeler</h3><p>Kanıt katmanı.</p><span class="meta">A1</span></a>
      <a class="card" href="/sektorler/"><h3>Sektörler</h3><p>Dikey girişler.</p><span class="meta">A1</span></a>
    </div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>İlgili hizmetler</h2>
    <div class="card-grid">{related_cards(s["related"])}</div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Sık sorulan sorular</h2>
    <div class="faq">{faq_html(s["faqs"])}</div>
    <p class="note" style="margin-top:28px;">EEAT: Gerçek lightbox / display / ofis / İSG uygulama fotoğrafları eklenmeden index riski yüksektir.</p>
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>{s["name"]} teklifi</h2>
    <a class="btn btn-primary" href="{w}" target="_blank" rel="noopener">WhatsApp</a>
    <a class="btn btn-ghost" href="tel:{PHONE_TEL}" style="margin-left:12px;">Ara</a>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "hizmetler" / s["slug"] / "index.html", html)


def patch_hizmetler_hub() -> None:
    """Insert/replace A2 section on existing hub without rewriting A0 cards."""
    path = ROOT / "hizmetler" / "index.html"
    if not path.exists():
        print("skip hub patch: hizmetler/index.html missing")
        return
    html = path.read_text(encoding="utf-8")
    cards = "\n".join(
        f'<a class="card" href="/hizmetler/{s["slug"]}/"><h3>{s["name"]}</h3>'
        f'<p>{s["lede"]}</p><span class="meta">A2 · /{s["slug"]}/</span></a>'
        for s in A2_SERVICES
    )
    section = f"""<section class="section-band paper-band" id="wave-a2">
  <div class="wrap">
    <h2>Wave A2 hizmetler</h2>
    <p class="intro">Lightbox, display/POS, ofis branding ve iş güvenliği — Phase 4 ownership kilitli.</p>
    <div class="card-grid">{cards}</div>
  </div>
</section>
"""
    if 'id="wave-a2"' in html:
        html = re.sub(
            r'<section class="section-band paper-band" id="wave-a2">.*?</section>',
            section.strip(),
            html,
            count=1,
            flags=re.S,
        )
    else:
        html = html.replace("</footer>", section + "</footer>")
        # place before footer
        html = html.replace(section + "</footer>", "")
        html = html.replace("<footer>", section + "<footer>")
    # Expand hub description lightly without changing H1
    html = html.replace(
        'content="Malt Studio hizmetleri: tabela, ışıklı tabela, kutu harf, totem, araç giydirme ve cam giydirme."',
        'content="Malt Studio hizmetleri: tabela, ışıklı tabela, kutu harf, totem, araç giydirme, cam giydirme, lightbox, display/POS, ofis branding, iş güvenliği tabelaları."',
    )
    path.write_text(html, encoding="utf-8")
    print("patched", path.relative_to(ROOT))


def merge_sitemap() -> None:
    urls = [
        f"{SITE}/",
        f"{SITE}/hizmetler/",
        f"{SITE}/bolgeler/tekirdag/",
        f"{SITE}/projeler/",
        f"{SITE}/sektorler/",
        f"{SITE}/bilgi/",
    ]
    for s in A0_SERVICES:
        urls.append(f"{SITE}/hizmetler/{s}/")
        urls.append(f"{SITE}/hizmet-bolge/tekirdag-{s}/")
    for s in A2_SERVICES:
        urls.append(f"{SITE}/hizmetler/{s['slug']}/")

    # Discover A1 leaves if present
    for folder, prefix in [
        ("projeler", "/projeler/"),
        ("sektorler", "/sektorler/"),
        ("bilgi", "/bilgi/"),
    ]:
        base = ROOT / folder
        if not base.exists():
            continue
        for p in sorted(base.glob("*/index.html")):
            urls.append(f"{SITE}{prefix}{p.parent.name}/")

    # dedupe preserve order
    seen = set()
    ordered = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            ordered.append(u)

    body = "\n".join(
        f"""  <url>
    <loc>{u}</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if u == SITE + "/" else "0.7"}</priority>
  </url>"""
        for u in ordered
    )
    (ROOT / "sitemap.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
""",
        encoding="utf-8",
    )
    print("wrote sitemap.xml", len(ordered), "urls")


def main() -> None:
    for s in A2_SERVICES:
        build_service(s)
    patch_hizmetler_hub()
    merge_sitemap()
    print("Wave A2 build complete.")


if __name__ == "__main__":
    main()
