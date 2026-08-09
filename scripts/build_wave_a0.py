#!/usr/bin/env python3
"""Generate Wave A0 static pages only. Ownership rules: Phase 4 QA."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://maltstudio.co"
PHONE_DISPLAY = "0552 582 69 59"
PHONE_TEL = "+905525826959"
WA = "905525826959"
EMAIL = "merhaba@maltstudio.com"

SERVICES = [
    {
        "slug": "tabela",
        "name": "Tabela",
        "pk": "tabela",
        "title": "Tabela | Üretim, Montaj ve Reklam Tabelası",
        "description": "Tabela üretimi ve montajı. Dış ve iç mekan tabela çözümleri, mağaza ve iş yeri tabelaları. Tekirdağ merkezli Malt Studio.",
        "lede": "İş yerinizi uzaktan okunur kılan, malzemesi ve montajı doğru planlanmış tabela sistemleri üretiyoruz.",
        "overview": "Tabela; markanın sokaktaki imzasıdır. Malt Studio olarak kompozit, ışıksız ve ışıklı seçeneklerle dış mekan ve iç mekan tabela üretimi yapıyoruz. Bu sayfa genel tabela hizmetini anlatır — Tekirdağ’a özel ticari aramalar için ayrı yerel sayfamız vardır.",
        "benefits": [
            "Ölçüye özel üretim ve saha keşfi",
            "Malzeme seçiminde dayanım / bütçe dengesi",
            "Montaj planı ve güvenlikli uygulama",
            "Marka görünürlüğü ile uyumlu tasarım",
        ],
        "apps": [
            "Mağaza ve dükkan cepheleri",
            "Ofis ve plaza girişleri",
            "Fabrika ve depo yön tabelaları",
            "Kurumsal tesis kimliği",
        ],
        "materials": "Kompozit panel, forex/PVC, vinil baskı uygulamaları, ışıklı ve ışıksız kasa sistemleri. Malzeme seçimi konum, rüzgâr yükü ve gece görünürlüğüne göre yapılır.",
        "process": "Keşif ve ölçü → tasarım onayı → üretim → kalite kontrol → yerinde montaj. Süre, ölçü ve izin süreçlerine bağlıdır.",
        "pricing": "Tabela fiyatını ölçüler, malzeme, ışıklı/ışıksız tercih, montaj yüksekliği ve saha koşulları belirler. Sabit katalog fiyatı yerine keşif sonrası net teklif veriyoruz.",
        "timeline": "Tipik işlerde tasarım onayı sonrası üretim ve montaj birkaç iş gününden birkaç haftaya kadar değişir.",
        "faqs": [
            ("Tabela ile ışıklı tabela aynı şey mi?", "Hayır. Bu sayfa genel tabela hizmetini kapsar. Işıklı tabela için ayrı hizmet sayfamız vardır."),
            ("Montajı siz mi yapıyorsunuz?", "Evet. Üretim ve yerinde montaj aynı ekip planıyla yürütülür."),
            ("Tekirdağ’da hizmet veriyor musunuz?", "Evet. Tekirdağ odaklı yerel sayfamızdan bölgeye özel bilgi alabilirsiniz."),
        ],
    },
    {
        "slug": "isikli-tabela",
        "name": "Işıklı Tabela",
        "pk": "ışıklı tabela",
        "title": "Işıklı Tabela | LED Tabela Üretimi ve Montajı",
        "description": "Işıklı tabela ve LED tabela üretimi. Gece görünür mağaza ve kurumsal tabelalar. Malt Studio.",
        "lede": "Gündüz markayı taşıyan, gece de okunur kalan ışıklı tabela sistemleri tasarlayıp üretiyoruz.",
        "overview": "Işıklı tabela; LED modül, kasa ve yüz malzemesinin birlikte çalıştığı bir üründür. Bu sayfa ışıklı tabela / LED tabela ticari niyetini hedefler. Lightbox (ışıklı kutu / SEG) ayrı bir ürün ailesidir ve Wave A0 kapsamında bu URL’de hedeflenmez.",
        "benefits": [
            "Gece görünürlük ve vitrin vurgusu",
            "LED verimli aydınlatma planı",
            "Cepheye uygun kasa derinlikleri",
            "Servis ve modül erişimi düşünülmüş üretim",
        ],
        "apps": [
            "Mağaza ve perakende cepheleri",
            "Plaza ve ofis girişleri",
            "Eczane / klinik / hizmet noktaları",
            "Kurumsal tesis kimliği",
        ],
        "materials": "Alüminyum kasa, LED modüller, güç kaynakları, akrilik/pleksi veya germe kumaş yüzeyler (ürüne göre).",
        "process": "Cephe analizi → aydınlatma ve ölçü → üretim → elektrik/montaj koordinasyonu → teslim.",
        "pricing": "Kasa ölçüsü, LED yoğunluğu, yüzey malzemesi ve montaj koşulları fiyatı belirler.",
        "timeline": "Onaylı tasarım sonrası tipik üretim-montaj süresi işin ölçeğine göre değişir; keşifte netlenir.",
        "faqs": [
            ("LED tabela ile neon aynı mı?", "Hayır. Neon ayrı bir formdur. Bu sayfa ışıklı / LED tabela içindir."),
            ("Lightbox arıyorum?", "Lightbox (ışıklı kutu) ayrı ürün dilidir; şimdilik ışıklı tabela keşfinde ihtiyacı birlikte netleştiriyoruz."),
            ("Arıza ve servis?", "LED ve güç kaynağı servisi için iletişime geçebilirsiniz. Ayrı montaj/servis sayfası sonraki dalgada gelecektir."),
        ],
    },
    {
        "slug": "kutu-harf",
        "name": "Kutu Harf",
        "pk": "kutu harf",
        "title": "Kutu Harf | Pleksi ve Paslanmaz Cephe Yazıları",
        "description": "Kutu harf üretimi ve montajı. Pleksi, paslanmaz ve ışıklı kutu harf çözümleri. Malt Studio.",
        "lede": "Cepheye derinlik ve prestij katan kutu harf sistemlerini ölçüye özel üretiyoruz.",
        "overview": "Kutu harf (channel letters), marka adını cephede üç boyutlu taşıyan harf sistemidir. Pleksi ve paslanmaz gibi malzeme seçenekleri bu hizmetin alt varyasyonlarıdır; Wave A0’da ayrı ürün URL’si açılmadan bu sayfada anlatılır.",
        "benefits": [
            "Cephede güçlü marka okunurluğu",
            "Işıklı veya ışıksız seçenekler",
            "Malzemeye göre uzun ömür",
            "Mimari ile uyumlu ölçü ve aralık",
        ],
        "apps": [
            "Plaza ve ofis cepheleri",
            "Mağaza isim yazıları",
            "Fabrika / tesis girişleri",
            "Resepsiyon arkası 3D logo uygulamaları (ilgili paketlerle)",
        ],
        "materials": "Pleksi/akrilik, paslanmaz, kompozit yan malzemeler, LED (ışıklı modellerde).",
        "process": "Font/marka dosyası → ölçü ve derinlik → kesim/üretim → cephe montajı.",
        "pricing": "Harf adedi, yükseklik, malzeme, ışıklı tercih ve montaj yüzeyi fiyatı belirler.",
        "timeline": "Onay sonrası üretim genellikle proje ölçeğine bağlıdır; keşifte planlanır.",
        "faqs": [
            ("Channel letters nedir?", "Kutu harfin uluslararası adıdır. Aynı hizmet ailesidir."),
            ("Pleksi mi paslanmaz mı?", "Bütçe, mimari ve bakım beklentisine göre seçilir; keşifte önerilir."),
            ("Paslanmaz ayrı sayfa mı?", "Wave A0’da bu hizmet altında anlatılır; gerekirse sonra ürün sayfasına ayrılır."),
        ],
    },
    {
        "slug": "totem",
        "name": "Totem",
        "pk": "totem tabela",
        "title": "Totem Tabela | Yol ve Tesis Totem Üretimi",
        "description": "Totem tabela üretimi ve montajı. Yol kenarı, tesis girişi ve yönlendirme totemleri. Malt Studio.",
        "lede": "Uzaktan görülen, yönlendiren ve kurumsal kimliği taşıyan totem tabela sistemleri üretiyoruz.",
        "overview": "Totem tabela; yol kenarı, tesis girişi ve otopark gibi noktalarda markayı ve yönü taşıyan dikey sistemdir. Pylon / monument gibi alt tipler Wave A0’da bu sayfanın parçasıdır — ayrı URL açılmaz.",
        "benefits": [
            "Uzaktan okunabilirlik",
            "Tesis ve yol yaklaşımında yönlendirme",
            "Işıklı seçeneklerle gece görünürlük",
            "Statik/montaj planına uygun üretim",
        ],
        "apps": [
            "Sanayi ve fabrika girişleri",
            "AVM / plaza yaklaşımı",
            "Akaryakıt ve yol kenarı noktaları",
            "Kurumsal kampüs yönlendirmesi",
        ],
        "materials": "Çelik/alüminyum konstrüksiyon, kompozit yüzeyler, ışıklı kasa seçenekleri.",
        "process": "Saha keşfi → yük/temel ihtiyacı → tasarım → imalat → vinçli/saha montajı.",
        "pricing": "Yükseklik, ışıklı tercih, temel/montaj koşulları ve yüzey alanı fiyatı belirler.",
        "timeline": "Temel ve izin gerektiren işlerde süre uzayabilir; plan keşifte çıkar.",
        "faqs": [
            ("Totem ile pylon farkı nedir?", "Pylon genelde daha yüksek yol kenarı sistemidir; bu sitede aynı hizmet ailesinde ele alınır."),
            ("İç mekân display totem?", "Taşınabilir fuar/display totemleri farklı bir üründür; bu sayfa dış mekân totem içindir."),
            ("OSB montajı yapıyor musunuz?", "Evet. Sanayi bölgelerinde keşif ve montaj planlanır."),
        ],
    },
    {
        "slug": "arac-giydirme",
        "name": "Araç Giydirme",
        "pk": "araç giydirme",
        "title": "Araç Giydirme | Filo ve Ticari Araç Kaplama",
        "description": "Araç giydirme ve filo kaplama. Ticari araç reklam giydirme uygulamaları. Malt Studio.",
        "lede": "Hareket halindeki marka yüzeyi: ticari araç ve filo giydirme uygulamaları.",
        "overview": "Araç giydirme; folyo baskı ve uygulama ile aracın mobil reklam yüzeyine dönüştürülmesidir. Full wrap ve parça giydirme bu hizmetin alt uygulamalarıdır.",
        "benefits": [
            "Filo genelinde tutarlı marka dili",
            "Cast/kalendered folyo seçenekleri",
            "Parça veya full kaplama",
            "Sökülebilir / yenilenebilir uygulamalar",
        ],
        "apps": [
            "Panelvan ve hafif ticari araçlar",
            "Kurumsal filo",
            "Servis ve dağıtım araçları",
            "Showroom / demo araçları",
        ],
        "materials": "Araç folyoları, laminasyon (ihtiyaca göre), dijital baskı.",
        "process": "Ölçü / şablon → tasarım → baskı → yüzey hazırlığı → uygulama.",
        "pricing": "Araç tipi, kaplama oranı, folyo kalitesi ve baskı alanı fiyatı belirler.",
        "timeline": "Tek araçta genelde kısa; filo işlerinde planlı takvim gerekir.",
        "faqs": [
            ("Folyo baskı ile aynı mı?", "Baskı üretim adımıdır; sonuç ürün araç giydirmedir. Bu sayfa sonucu hedefler."),
            ("Boyayı bozar mı?", "Doğru folyo ve uygulama ile kontrollü söküm mümkündür; araç yüzeyine göre değerlendirilir."),
            ("Filo indirimi?", "Toplu filo işlerinde kurumsal teklif hazırlanır."),
        ],
    },
    {
        "slug": "cam-giydirme",
        "name": "Cam Giydirme",
        "pk": "cam giydirme",
        "title": "Cam Giydirme | One Way Vision ve Vitrin Folyosu",
        "description": "Cam giydirme, one way vision ve vitrin folyo uygulamaları. Mağaza cam reklamı. Malt Studio.",
        "lede": "Vitrin ve cam yüzeylerde görünürlük, gizlilik ve marka mesajını dengeleyen giydirme uygulamaları.",
        "overview": "Cam giydirme; one way vision, transparan/folyo baskı ve vitrin grafiklerini kapsar. ‘Window graphics’, ‘cam yazısı’, ‘vitrin reklamı’ aynı aileye aittir — ayrı URL açılmaz.",
        "benefits": [
            "İçeriden görüş / dışarıdan grafik dengesi (OWV)",
            "Mağaza mesajı ve kampanya alanı",
            "Gizlilik folyosu seçenekleri",
            "Hızlı yenilenebilir kampanya yüzeyleri",
        ],
        "apps": [
            "Mağaza ve dükkan vitrinleri",
            "Ofis cam bölmeleri",
            "Showroom cephe camları",
            "Kampanya dönemleri",
        ],
        "materials": "One way vision, transparan folyo, kumlama/frosted folyo, baskılı vinil.",
        "process": "Ölçü → tasarım → baskı/kesim → cam temizliği → uygulama.",
        "pricing": "m² alanı, folyo tipi ve uygulama zorluğu fiyatı belirler.",
        "timeline": "Çoğu vitrin işi kısa sürede tamamlanır; keşifte netlenir.",
        "faqs": [
            ("One way vision nedir?", "Dışarıdan baskı görünen, içeriden bakışa izin veren delikli folyodur."),
            ("Ofis gizlilik folyosu?", "Cam giydirme ailesindedir; ofis paket ihtiyacı ayrıca konuşulur."),
            ("Araç camı?", "Araç camı uygulamaları araç giydirme kapsamında değerlendirilir."),
        ],
    },
]

# Sibling order for internal links (exclude self)
SERVICE_ORDER = [s["slug"] for s in SERVICES]


def wa_link(msg: str) -> str:
    from urllib.parse import quote

    return f"https://wa.me/{WA}?text={quote(msg)}"


def logo_svg() -> str:
    return (
        '<img class="logo-mark" src="/images/logo.svg" width="120" height="19" '
        'alt="Malt Studio" onerror="this.style.display=\'none\'">'
    )


def head(title: str, description: str, canonical: str, og_title: str | None = None) -> str:
    ot = og_title or title
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
<meta property="og:title" content="{ot}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="tr_TR">
<meta property="og:image" content="{SITE}/images/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ot}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE}/images/og.jpg">
<link rel="icon" type="image/png" href="/images/icon-192.png">
<link rel="apple-touch-icon" href="/images/icon-192.png">
<link rel="manifest" href="/manifest.json">
<link rel="preload" href="/assets/fonts/big-shoulders-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/big-shoulders-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts.css">
<link rel="stylesheet" href="/assets/site.css">
</head>
"""


def header_nav() -> str:
    return f"""<header>
  <a href="/" aria-label="Malt Studio ana sayfa">{logo_svg()}</a>
  <nav>
    <a href="/hizmetler/">Hizmetler</a>
    <a href="/bolgeler/tekirdag/">Tekirdağ</a>
    <a href="/#iletisim">İletişim</a>
    <a href="tel:{PHONE_TEL}">Ara</a>
  </nav>
</header>
"""


def footer() -> str:
    service_links = "\n".join(
        f'<li><a href="/hizmetler/{s["slug"]}/">{s["name"]}</a></li>' for s in SERVICES
    )
    sxc_links = "\n".join(
        f'<li><a href="/hizmet-bolge/tekirdag-{s["slug"]}/">Tekirdağ {s["name"]}</a></li>'
        for s in SERVICES
    )
    return f"""<footer>
  <div class="wrap">
    <div class="footer-top">
      <div>
        <div class="footer-logo">{logo_svg()}</div>
        <p style="font-size:14px;line-height:1.6;color:rgba(241,238,231,0.65);max-width:280px;">
          Tekirdağ merkezli reklam ve tabela üreticisi. Marka görünürlüğü için üretim ve montaj.
        </p>
      </div>
      <div>
        <h4>Hizmetler</h4>
        <ul>{service_links}</ul>
      </div>
      <div>
        <h4>Tekirdağ</h4>
        <ul>
          <li><a href="/bolgeler/tekirdag/">Tekirdağ Rehberi</a></li>
          {sxc_links}
        </ul>
      </div>
      <div>
        <h4>İletişim</h4>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Tekirdağ, Türkiye</li>
          <li><a href="/#iletisim">Mesaj bırakın</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2025–2026 Malt Studio</span>
      <span>Wave A0 · Ownership-locked IA</span>
    </div>
  </div>
</footer>
<a class="whatsapp-btn" href="{wa_link("Merhaba, Malt Studio hizmetleri hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
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


def sibling_cards(current: str) -> str:
    cards = []
    for s in SERVICES:
        if s["slug"] == current:
            continue
        cards.append(
            f'<a class="card" href="/hizmetler/{s["slug"]}/"><h3>{s["name"]}</h3>'
            f'<p>{s["lede"][:90]}…</p><span class="meta">Hizmet</span></a>'
        )
    return "\n".join(cards[:5])


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def build_hizmetler_hub() -> None:
    cards = "\n".join(
        f'<a class="card" href="/hizmetler/{s["slug"]}/"><h3>{s["name"]}</h3>'
        f'<p>{s["lede"]}</p><span class="meta">/{s["slug"]}/</span></a>'
        for s in SERVICES
    )
    sxc = "\n".join(
        f'<a class="card" href="/hizmet-bolge/tekirdag-{s["slug"]}/">'
        f"<h3>Tekirdağ {s['name']}</h3>"
        f"<p>Yerel ticari sayfa — geo-money owner.</p>"
        f'<span class="meta">S×C</span></a>'
        for s in SERVICES
    )
    canonical = f"{SITE}/hizmetler/"
    html = f"""{head("Hizmetler | Tabela, Işıklı Tabela, Kutu Harf ve Daha Fazlası", "Malt Studio hizmetleri: tabela, ışıklı tabela, kutu harf, totem, araç giydirme ve cam giydirme.", canonical)}
<body>
{header_nav()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Hizmetler", None))}
    <div class="eyebrow">Wave A0 · Core Services</div>
    <h1>Hizmetler</h1>
    <p class="lede">Parasal niyetli çekirdek hizmetler. Her hizmetin bir sahibi URL’si vardır; Tekirdağ geo-money sayfaları ayrıdır.</p>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Çekirdek hizmetler</h2>
    <p class="intro">Non-geo ticari başlıklar bu sayfalarda yaşar.</p>
    <div class="card-grid">{cards}</div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>Tekirdağ yerel sayfalar</h2>
    <p class="intro">“Tekirdağ + hizmet” aramalarının sahibi S×C sayfalarıdır — hizmet sayfası değil.</p>
    <div class="card-grid">{sxc}</div>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "hizmetler" / "index.html", html)


def build_service(s: dict) -> None:
    canonical = f"{SITE}/hizmetler/{s['slug']}/"
    sxc_href = f"/hizmet-bolge/tekirdag-{s['slug']}/"
    benefits = "".join(f"<li>{b}</li>" for b in s["benefits"])
    apps = "".join(f"<li>{a}</li>" for a in s["apps"])
    wa = wa_link(f"Merhaba, {s['name']} hizmeti hakkında bilgi almak istiyorum.")
    html = f"""{head(s["title"], s["description"], canonical)}
<body>
{header_nav()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Hizmetler", "/hizmetler/"), (s["name"], None))}
    <div class="eyebrow">Hizmet · Non-geo owner</div>
    <h1>{s["name"]}</h1>
    <p class="lede">{s["lede"]}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_DISPLAY}</a>
      <a class="btn btn-ghost" href="{sxc_href}">Tekirdağ {s["name"]}</a>
    </div>
    <div class="trust-strip">
      <span><strong>Owner PK:</strong> {s["pk"]}</span>
      <span><strong>Geo PK:</strong> → {sxc_href}</span>
      <span><strong>Üretim + montaj</strong></span>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    <div class="content-block">
      <h2>Bu hizmet nedir?</h2>
      <p>{s["overview"]}</p>
      <p class="note">Ownership: Bu sayfa “{s["pk"]}” birincil sahibidir. “Tekirdağ {s["name"].lower()}” birincil hedefi değildir — o niyet {sxc_href} sayfasındadır.</p>
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
    <h2>Tekirdağ’da bu hizmet</h2>
    <p class="intro">Yerel ticari niyet ve firma aramaları için coğrafi sayfaya gidin.</p>
    <div class="card-grid">
      <a class="card" href="{sxc_href}"><h3>Tekirdağ {s["name"]}</h3><p>Geo-money owner sayfa.</p><span class="meta">S×C</span></a>
      <a class="card" href="/bolgeler/tekirdag/"><h3>Tekirdağ Bölge</h3><p>Şehir hub’ı — firma ve yakın niyet.</p><span class="meta">City</span></a>
      <a class="card" href="/hizmetler/"><h3>Tüm hizmetler</h3><p>Wave A0 çekirdek liste.</p><span class="meta">Hub</span></a>
    </div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>İlgili hizmetler</h2>
    <p class="intro">Kardeş hizmetler — birbirinin birincil anahtar kelimesini çalmaz.</p>
    <div class="card-grid">{sibling_cards(s["slug"])}</div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Sık sorulan sorular</h2>
    <div class="faq">{faq_html(s["faqs"])}</div>
    <p class="note" style="margin-top:28px;">Proje galerisi ve saha fotoğrafları sonraki içerik dalgasında eklenecektir. EEAT için gerçek iş görselleri zorunludur.</p>
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>{s["name"]} için keşif veya teklif alın</h2>
    <a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    <a class="btn btn-ghost" href="tel:{PHONE_TEL}" style="margin-left:12px;">Ara</a>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "hizmetler" / s["slug"] / "index.html", html)


def build_city() -> None:
    canonical = f"{SITE}/bolgeler/tekirdag/"
    service_cards = "\n".join(
        f'<a class="card" href="/hizmetler/{s["slug"]}/"><h3>{s["name"]}</h3>'
        f"<p>Non-geo hizmet sayfası.</p><span class=\"meta\">Hizmet</span></a>"
        for s in SERVICES
    )
    sxc_cards = "\n".join(
        f'<a class="card" href="/hizmet-bolge/tekirdag-{s["slug"]}/">'
        f"<h3>Tekirdağ {s['name']}</h3>"
        f"<p>Yerel ticari owner.</p><span class=\"meta\">S×C</span></a>"
        for s in SERVICES
    )
    faqs = [
        (
            "Tekirdağ’da tabela firması mısınız?",
            "Evet. Malt Studio Tekirdağ merkezli reklam ve tabela üretimidir. Spesifik hizmet+şehir aramaları ilgili S×C sayfalarındadır.",
        ),
        (
            "Süleymanpaşa için ayrı sayfa var mı?",
            "Hayır. Süleymanpaşa / Tekirdağ merkez, Tekirdağ hub ve Tekirdağ S×C sayfalarına alias olarak bağlanır — paralel URL açılmaz.",
        ),
        (
            "Çorlu veya Çerkezköy sayfaları?",
            "Wave A0 dışındadır. Sonraki dalgada açılacaktır.",
        ),
        (
            "Keşif için geliyor musunuz?",
            "Tekirdağ ve çevre ilçelerde keşif ve montaj planlanır. WhatsApp veya telefon ile yazın.",
        ),
    ]
    wa = wa_link("Merhaba, Tekirdağ'da hizmetleriniz hakkında bilgi almak istiyorum.")
    html = f"""{head(
        "Tekirdağ Reklam ve Tabela | Yerel Hizmet Rehberi",
        "Tekirdağ reklam firması ve tabela üreticisi Malt Studio. İlçe hizmetleri, yerel çözümler ve iletişim.",
        canonical,
    )}
<body>
{header_nav()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Bölgeler", None), ("Tekirdağ", None))}
    <div class="eyebrow">City hub · Local / firm owner</div>
    <h1>Tekirdağ Reklam &amp; Tabela</h1>
    <p class="lede">Tekirdağ’da üreten ve uygulayan bir reklam–tabela ekibiyle çalışın. Bu sayfa yerel firma ve bölge niyetini taşır; tek bir hizmetin geo-money başlığını çalmaz.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_DISPLAY}</a>
      <a class="btn btn-ghost" href="/hizmetler/">Hizmetler</a>
    </div>
    <div class="trust-strip">
      <span><strong>Owner:</strong> Tekirdağ firma / yerel hub</span>
      <span><strong>NAP:</strong> Tekirdağ, Türkiye</span>
      <span><strong>Alias:</strong> Süleymanpaşa → bu hub</span>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    <div class="content-block">
      <h2>Tekirdağ’da ne sunuyoruz?</h2>
      <p>Malt Studio; tabela, ışıklı tabela, kutu harf, totem, araç giydirme ve cam giydirme başta olmak üzere markanın sahadaki görünürlüğünü üretir. Merkezimiz Tekirdağ’dadır. Süleymanpaşa / merkez aramaları bu sayfa ve Tekirdağ S×C sayfalarına yönlenir.</p>
      <p>Sanayi koridoru (Çorlu, Çerkezköy ve çevresi) için ayrı şehir sayfaları sonraki dalgadadır; bugün iletişim ve keşif Tekirdağ üssünden yürütülür.</p>
    </div>
    <div class="content-block">
      <h2>Yerel kanıt notu</h2>
      <p class="note">Wave A0’da proje detay sayfaları ve saha fotoğrafları henüz yayınlanmadı. Yerel EEAT için gerçek Tekirdağ / çevre iş görselleri ve proje URL’leri bir sonraki önceliktir. Bu sayfa yapısal olarak doğrudur; kanıt katmanı eksiktir.</p>
    </div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Tekirdağ hizmet × şehir sayfaları</h2>
    <p class="intro">“Tekirdağ tabela”, “Tekirdağ ışıklı tabela” gibi aramaların birincil sahibi buradaki S×C sayfalarıdır.</p>
    <div class="card-grid">{sxc_cards}</div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>Hizmet sayfaları</h2>
    <p class="intro">Coğrafyasız ticari başlıklar.</p>
    <div class="card-grid">{service_cards}</div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Sık sorulan sorular</h2>
    <div class="faq">{faq_html(faqs)}</div>
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>Tekirdağ’da keşif veya teklif</h2>
    <a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    <a class="btn btn-ghost" href="tel:{PHONE_TEL}" style="margin-left:12px;">Ara</a>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "bolgeler" / "tekirdag" / "index.html", html)


def build_sxc(s: dict) -> None:
    slug = f"tekirdag-{s['slug']}"
    canonical = f"{SITE}/hizmet-bolge/{slug}/"
    name = s["name"]
    local_pk = f"tekirdağ {s['pk']}"
    wa = wa_link(f"Merhaba, Tekirdağ {name} hakkında bilgi almak istiyorum.")
    other_sxc = "\n".join(
        f'<a class="card" href="/hizmet-bolge/tekirdag-{o["slug"]}/">'
        f"<h3>Tekirdağ {o['name']}</h3><p>İlgili yerel sayfa.</p><span class=\"meta\">S×C</span></a>"
        for o in SERVICES
        if o["slug"] != s["slug"]
    )
    faqs = [
        (
            f"Tekirdağ’da {name.lower()} yaptırabilir miyim?",
            f"Evet. Bu sayfa Tekirdağ {name.lower()} ticari niyetinin birincil sahibidir. Keşif ve montaj Tekirdağ üssünden planlanır.",
        ),
        (
            "Genel hizmet sayfası ile farkı nedir?",
            f"Genel /hizmetler/{s['slug']}/ sayfası coğrafyasız “{s['pk']}” niyetini taşır. Bu sayfa “{local_pk}” niyetini taşır.",
        ),
        (
            "Fiyatı neye göre çıkar?",
            s["pricing"],
        ),
        (
            "Süleymanpaşa geçerli mi?",
            "Evet. Süleymanpaşa / merkez talepleri Tekirdağ S×C sayfalarına bağlanır; ayrı URL yoktur.",
        ),
    ]
    # Unique local angle per service (anti-doorway)
    local_angles = {
        "tabela": "Tekirdağ merkez ve ilçe çarşılarında mağaza cepheleri, plaza girişleri ve iş yeri tabelaları için ölçü-montaj odaklı çalışıyoruz. Süleymanpaşa alias’ı bu sayfaya dahildir.",
        "isikli-tabela": "Tekirdağ’da gece de açık kalan ticaret noktaları ve plaza cepheleri için LED ışıklı tabela üretip montajlıyoruz. Lightbox ayrı üründür; bu sayfa ışıklı tabela geo-money sahibidir.",
        "kutu-harf": "Tekirdağ’daki plaza, ofis ve mağaza cephelerinde kilitlemeli kutu harf uygulamaları yapıyoruz. Channel letters aynı ailede değerlendirilir.",
        "totem": "Tekirdağ çevre yolu ve tesis girişlerinde okunur totem sistemleri için saha keşfi ve montaj planı çıkarıyoruz. OSB koridoru talepleri de Tekirdağ üssünden yönetilir.",
        "arac-giydirme": "Tekirdağ merkezli filolar ve ticari araçlar için giydirme uyguluyoruz. Lojistik ve servis araçlarında parça veya full kaplama seçenekleri sunulur.",
        "cam-giydirme": "Tekirdağ mağaza vitrinleri ve ofis camlarında one way vision ve folyo uygulamaları yapıyoruz. Kampanya dönemlerinde hızlı yenileme mümkündür.",
    }
    angle = local_angles[s["slug"]]
    html = f"""{head(
        f"Tekirdağ {name} | Yerel Üretim ve Montaj",
        f"Tekirdağ {name.lower()} üretimi ve montajı. {s['description']}",
        canonical,
    )}
<body>
{header_nav()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(
        ("Ana Sayfa", "/"),
        ("Hizmetler", "/hizmetler/"),
        (name, f"/hizmetler/{s['slug']}/"),
        (f"Tekirdağ {name}", None),
    )}
    <div class="eyebrow">Service × City · Geo-money owner</div>
    <h1>Tekirdağ {name}</h1>
    <p class="lede">{angle}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_DISPLAY}</a>
      <a class="btn btn-ghost" href="/hizmetler/{s['slug']}/">{name} hizmeti</a>
    </div>
    <div class="trust-strip">
      <span><strong>Owner PK:</strong> {local_pk}</span>
      <span><strong>Parent:</strong> /hizmetler/{s['slug']}/</span>
      <span><strong>City:</strong> /bolgeler/tekirdag/</span>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    <div class="content-block">
      <h2>Tekirdağ’da {name.lower()} kapsamı</h2>
      <p>{s["overview"]}</p>
      <p>{angle}</p>
      <p class="note">Anti-doorway: Bu sayfa ebeveyn hizmetin kopyası değildir. Yerel operasyon, lojistik ve Tekirdağ talep bağlamı eklenmiştir. Yine de gerçek proje fotoğrafları olmadan EEAT zayıf kalır.</p>
    </div>
    <div class="content-block">
      <h2>Yerel uygulamalar</h2>
      <ul>{''.join(f'<li>{a}</li>' for a in s['apps'])}</ul>
    </div>
    <div class="content-block">
      <h2>Üretim ve montaj lojistiği</h2>
      <p>{s["process"]} Tekirdağ üssünden keşif, üretim ve saha montajı koordine edilir. Süleymanpaşa / merkez talepleri aynı operasyonel plana girer.</p>
    </div>
    <div class="content-block">
      <h2>Fiyatı neler etkiler? (yerel)</h2>
      <p>{s["pricing"]} Tekirdağ içi erişim genelde standarttır; çevre ilçe ve OSB sahalarında montaj lojistiği teklife yansır.</p>
    </div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Kanıt ve projeler</h2>
    <p class="intro">Wave A0’da proje URL’leri henüz yok. Bu blok bilerek boş bırakılmadı — eksiklik şeffaf işaretlendi.</p>
    <p class="note">Eksik: Tekirdağ etiketli proje sayfaları, saha fotoğrafları, before/after. Index kararı yayın skor kartına bağlıdır.</p>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>Üst bağlantılar</h2>
    <div class="card-grid">
      <a class="card" href="/hizmetler/{s['slug']}/"><h3>{name}</h3><p>Non-geo hizmet owner.</p><span class="meta">Parent</span></a>
      <a class="card" href="/bolgeler/tekirdag/"><h3>Tekirdağ</h3><p>Şehir hub.</p><span class="meta">City</span></a>
      <a class="card" href="/hizmetler/"><h3>Hizmetler</h3><p>Çekirdek liste.</p><span class="meta">Hub</span></a>
    </div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>İlgili Tekirdağ sayfaları</h2>
    <div class="card-grid">{other_sxc}</div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>Sık sorulan sorular</h2>
    <div class="faq">{faq_html(faqs)}</div>
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>Tekirdağ {name} teklifi</h2>
    <a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    <a class="btn btn-ghost" href="tel:{PHONE_TEL}" style="margin-left:12px;">Ara</a>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "hizmet-bolge" / slug / "index.html", html)


def build_sitemap() -> None:
    urls = [f"{SITE}/", f"{SITE}/hizmetler/", f"{SITE}/bolgeler/tekirdag/"]
    for s in SERVICES:
        urls.append(f"{SITE}/hizmetler/{s['slug']}/")
        urls.append(f"{SITE}/hizmet-bolge/tekirdag-{s['slug']}/")
    body = "\n".join(
        f"""  <url>
    <loc>{u}</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if u == SITE + "/" else "0.8"}</priority>
  </url>"""
        for u in urls
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
"""
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("wrote sitemap.xml", len(urls), "urls")


def main() -> None:
    build_hizmetler_hub()
    for s in SERVICES:
        build_service(s)
        build_sxc(s)
    build_city()
    build_sitemap()
    print("Wave A0 build complete.")


if __name__ == "__main__":
    main()
