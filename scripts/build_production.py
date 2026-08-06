#!/usr/bin/env python3
"""Upgrade all existing URLs to production depth. No new URLs."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_site import (  # noqa: E402
    A0,
    A2,
    ALL_SERVICES,
    PHONE_DISPLAY,
    PHONE_TEL,
    ROOT,
    SITE,
    cards,
    crumbs,
    cta_band,
    eeat_block,
    evidence_gallery,
    faq_html,
    footer,
    head,
    header,
    mid_cta,
    process_steps,
    project_cta,
    project_placeholders,
    related_rail,
    wa,
    write,
)
from project_cases_a4 import CASES, INDUSTRY_LABEL, KNOWLEDGE_BY_SERVICE  # noqa: E402
from a5_copy import (  # noqa: E402
    ARTICLE_A5,
    ARTICLE_EXPAND,
    INDUSTRY_A5,
    INDUSTRY_EXPAND,
    SERVICE_A5,
    SERVICE_EXPAND,
    SERVICE_EXPAND2,
    ARTICLE_BRIDGE,
    ARTICLE_LONG,
    INDUSTRY_BRIDGE,
    INDUSTRY_LONG,
    SERVICE_BRIDGE,
    SERVICE_NUDGE,
    SERVICE_CHECKLIST,
    SERVICE_LONG,
    SERVICE_LONG2,
    SERVICE_INDUSTRIES,
)

# ---------------------------------------------------------------------------
# Inventory (frozen — do not add)
# ---------------------------------------------------------------------------
PROJECTS = [
    ("liman-kahve", "Liman Kahve", "restoran-cafe", ["isikli-tabela", "cam-giydirme", "tabela"]),
    ("volt-enerji", "Volt Enerji", "fabrika-osb", ["totem", "tabela", "kutu-harf"]),
    ("kuzey-tekstil", "Kuzey Tekstil", "fabrika-osb", ["tabela", "arac-giydirme", "totem"]),
    ("mera-otel", "Mera Otel", "plaza-ofis", ["kutu-harf", "isikli-tabela", "tabela"]),
    ("dortnal", "Dörtnal", "perakende", ["isikli-tabela", "cam-giydirme", "tabela"]),
    ("ekip-yazilim", "Ekip Yazılım", "plaza-ofis", ["kutu-harf", "cam-giydirme", "ofis-branding"]),
]
INDUSTRIES = [
    ("fabrika-osb", "Fabrika & OSB", "fabrika tabela"),
    ("restoran-cafe", "Restoran & Cafe", "restoran tabela"),
    ("saglik", "Sağlık", "klinik tabela"),
    ("plaza-ofis", "Plaza & Ofis", "ofis tabela"),
    ("insaat-santiye", "İnşaat & Şantiye", "şantiye brandası"),
    ("perakende", "Perakende", "mağaza tabelası"),
]
ARTICLES = [
    ("tabela-cesitleri", "Tabela Çeşitleri: Hangisi Ne İşe Yarar?", "tabela", "tabela çeşitleri"),
    ("isikli-mi-isiksiz-mi", "Işıklı Tabela mı Işıksız mı?", "isikli-tabela", "ışıklı mı ışıksız mı"),
    ("kutu-harf-malzemeler", "Kutu Harf Malzemeleri: Pleksi mi Paslanmaz mı?", "kutu-harf", "kutu harf malzemeleri"),
    ("one-way-vision-nedir", "One Way Vision Nedir?", "cam-giydirme", "one way vision nedir"),
    ("arac-giydirme-rehberi", "Araç Giydirme Rehberi: Süreç, Ömür, Filo", "arac-giydirme", "araç giydirme süreci"),
    ("tabela-fiyati", "Tabela Fiyatını Neler Etkiler?", "tabela", "tabela fiyatını neler etkiler"),
    ("totem-secim-rehberi", "Totem Tabela Seçim Rehberi", "totem", "totem tabela nasıl seçilir"),
]


def p(*paras: str) -> str:
    return "\n".join(f"<p>{x}</p>" for x in paras if x)


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def block(title: str, body_html: str) -> str:
    return f'<div class="content-block"><h2>{title}</h2>{body_html}</div>'


def depth_pad(topic: str, focus: str) -> str:
    """Wave A5: generic pad retired — unique a5_copy blocks replace filler."""
    return ""


# ===========================================================================
# SERVICE + S×C content seeds
# ===========================================================================
SERVICE_DEPTH = {
    "tabela": {
        "h1": "Tabela",
        "pk": "tabela",
        "title": "Tabela | Üretim, Montaj ve Reklam Tabelası",
        "desc": "Tabela üretimi ve montajı. Dış-iç mekan, mağaza ve tesis tabelaları. Tekirdağ merkezli Malt Studio.",
        "lede": "Ölçüye özel tabela üretimi: doğru malzeme, okunur tasarım ve güvenli montaj.",
        "extra": [
            "Tabela, markanın sokaktaki ve tesis girişindeki kalıcı imzasıdır. Doğru tabela; mesafeden okunur, malzemesi sahaya uygundur ve montajı uzun ömürlü planlanır.",
            "Işıksız kompozit tabeladan ışıklı sistemlere, iç yön tabelasından cephe kimliğine kadar ihtiyaçlar değişir. Bu sayfa coğrafyasız ‘tabela’ ticari niyetinin sahibidir.",
            "Tekirdağ’a özel aramalar (/hizmet-bolge/tekirdag-tabela/) ayrı URL’de tutulur; böylece hizmet ve yerel sayfa birbirini yemez.",
            "Keşifte ölçüler, montaj yüzeyi, rüzgâr/yükseklik ve gece görünürlük ihtiyacı birlikte değerlendirilir. Katalog fiyatı yerine sahaya göre teklif çıkarılır.",
            "Üretim atölyede, uygulama sahada tamamlanır. Teslimden sonra yenileme veya ek tabela talepleri aynı hat üzerinden planlanabilir.",
        ],
        "apps": ["Mağaza ve dükkan cepheleri", "Plaza / ofis girişleri", "Fabrika ve depo", "Kurumsal tesis kimliği", "İç mekan bilgilendirme"],
        "materials": "Kompozit panel, forex/PVC, vinil baskı, ışıklı/ışıksız kasa seçenekleri. Malzeme; konum, dayanım ve bütçeye göre seçilir.",
        "related_projects": ["liman-kahve", "volt-enerji", "dortnal"],
        "related_services": ["isikli-tabela", "kutu-harf", "totem", "cam-giydirme"],
        "bilgi": ["/bilgi/tabela-cesitleri/", "/bilgi/tabela-fiyati/"],
        "faqs": [
            ("Tabela ile ışıklı tabela farkı nedir?", "Işıklı tabela gece görünürlük için LED’li sistemdir; ayrı sayfası vardır. Bu sayfa genel tabela hizmetini kapsar."),
            ("Montajı siz yapıyor musunuz?", "Evet. Üretim ve yerinde montaj birlikte planlanır."),
            ("Fiyat listesi var mı?", "Hayır. Ölçü, malzeme ve montaj keşiften sonra netleşir."),
            ("Tekirdağ dışında çalışıyor musunuz?", "Tekirdağ üssünden çevre ilçelere keşif ve montaj planlanır."),
            ("Ne kadar sürer?", "Onay ve ölçüye göre birkaç iş gününden birkaç haftaya değişir."),
            ("Tasarım desteği var mı?", "Marka dosyanız yoksa sade ve okunur tasarım önerisi sunulur."),
            ("Eski tabela sökümü?", "Yenileme işlerinde söküm planlanabilir."),
            ("Garanti?", "Malzeme ve işçilik kapsamı teklifte yazılı netleştirilir."),
        ],
    },
    "isikli-tabela": {
        "h1": "Işıklı Tabela",
        "pk": "ışıklı tabela",
        "title": "Işıklı Tabela | LED Tabela Üretimi ve Montajı",
        "desc": "Işıklı tabela ve LED tabela üretimi-montajı. Gece görünür mağaza ve kurumsal tabelalar.",
        "lede": "Gündüz taşıyan, gece de okunan LED ışıklı tabela sistemleri.",
        "extra": [
            "Işıklı tabela; kasa, LED modül, güç kaynağı ve yüzey malzemesinin birlikte çalıştığı bir üründür. Amaç gece saatlerinde de markayı okunur kılmaktır.",
            "Bu sayfa ‘ışıklı tabela / LED tabela’ sahibidir. Lightbox (ışıklı kutu / SEG) ayrı üründür ve /hizmetler/lightbox/ altındadır.",
            "Cephe derinliği, elektrik hattı ve servis erişimi keşifte kontrol edilir. Yanlış LED yoğunluğu hem ışığı bozar hem servisi zorlaştırır.",
            "Mağaza, eczane, klinik ve plaza girişlerinde gece trafiği varsa ışıklı sistem çoğu zaman doğru yatırımdır.",
            "Tekirdağ geo-money niyeti /hizmet-bolge/tekirdag-isikli-tabela/ sayfasındadır.",
        ],
        "apps": ["Mağaza cepheleri", "Plaza girişleri", "Klinik / eczane", "Hizmet noktaları", "Kurumsal tesisler"],
        "materials": "Alüminyum kasa, LED modül, SMPS, akrilik/pleksi veya uygun yüzeyler.",
        "related_projects": ["liman-kahve", "dortnal", "mera-otel"],
        "related_services": ["tabela", "lightbox", "kutu-harf", "cam-giydirme"],
        "bilgi": ["/bilgi/isikli-mi-isiksiz-mi/", "/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("LED tabela neon mu?", "Hayır. Neon ayrı formdur."),
            ("Lightbox istiyorum?", "Lightbox ayrı sayfadadır: /hizmetler/lightbox/."),
            ("Elektrik hazır değilse?", "Keşifte altyapı ihtiyacı konuşulur."),
            ("Servis ve arıza?", "LED/güç kaynağı servisi için iletişime geçilir."),
            ("Fiyatı neye göre?", "Ölçü, LED, yüzey ve montaj koşulları."),
            ("Su ve toz?", "Dış mekân kasalarında sızdırmazlık planı yapılır."),
            ("Gece çok mu parlak olur?", "LED yoğunluğu cepheye göre ayarlanır."),
            ("Süre?", "Onay sonrası ölçeğe göre netlenir."),
        ],
    },
    "kutu-harf": {
        "h1": "Kutu Harf",
        "pk": "kutu harf",
        "title": "Kutu Harf | Pleksi ve Paslanmaz Cephe Yazıları",
        "desc": "Kutu harf üretimi ve montajı. Pleksi, paslanmaz ve ışıklı kutu harf.",
        "lede": "Cepheye derinlik katan ölçüye özel kutu harf sistemleri.",
        "extra": [
            "Kutu harf (channel letters), marka adını üç boyutlu taşıyan cephe yazısıdır. Pleksi ve paslanmaz en sık malzeme aileleridir.",
            "Bu sayfa ‘kutu harf’ sahibidir. Channel letters ayrı URL açılmaz; aynı ailede anlatılır.",
            "Harf yüksekliği, derinlik, ışıklı/ışıksız tercih ve montaj yüzeyi okunurluğu belirler.",
            "Plaza, ofis ve mağaza cephelerinde prestij algısını en hızlı yükselten uygulamalardan biridir.",
            "Tekirdağ yerel niyeti /hizmet-bolge/tekirdag-kutu-harf/ sayfasındadır.",
        ],
        "apps": ["Plaza cepheleri", "Mağaza isim yazıları", "Ofis girişleri", "Fabrika girişi", "Resepsiyon 3D logo"],
        "materials": "Pleksi/akrilik, paslanmaz, LED (ışıklı modeller), yan/montaj aparatları.",
        "related_projects": ["mera-otel", "ekip-yazilim", "volt-enerji"],
        "related_services": ["ofis-branding", "isikli-tabela", "tabela", "lightbox"],
        "bilgi": ["/bilgi/kutu-harf-malzemeler/", "/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("Pleksi mi paslanmaz mı?", "Bütçe, mimari ve bakım beklentisine göre; rehber sayfada karşılaştırılır."),
            ("Channel letters nedir?", "Kutu harfin uluslararası adıdır."),
            ("Işıklı olur mu?", "Evet, modele göre LED’li üretilir."),
            ("Font şart mı?", "Vektörel logo/font dosyası kaliteyi yükseltir."),
            ("Montaj her yüzeye olur mu?", "Keşif şarttır."),
            ("Bakım?", "Dış ortamda periyodik kontrol önerilir."),
            ("Süre?", "Harf adedi ve malzemeye göre değişir."),
            ("Ofis içi logo?", "Ofis branding paketiyle birlikte planlanabilir."),
        ],
    },
    "totem": {
        "h1": "Totem",
        "pk": "totem tabela",
        "title": "Totem Tabela | Yol ve Tesis Totem Üretimi",
        "desc": "Totem tabela üretimi ve montajı. Tesis girişi ve yol kenarı sistemleri.",
        "lede": "Uzaktan görülen, yönlendiren totem tabela sistemleri.",
        "extra": [
            "Totem; yol kenarı, tesis girişi ve otopark yaklaşımında markayı ve yönü taşır.",
            "Pylon/monument alt tipleri bu sayfada anlatılır; ayrı doorway URL açılmaz.",
            "Taşınabilir indoor display totem /hizmetler/display-pos/ ailesindedir.",
            "Yükseklik, temel, ışıklı tercih ve görüş mesafesi keşifte hesaplanır.",
            "Tekirdağ geo sayfası: /hizmet-bolge/tekirdag-totem/.",
        ],
        "apps": ["Fabrika/OSB girişi", "Plaza yaklaşımı", "Yol kenarı", "Otopark", "Kurumsal kampüs"],
        "materials": "Çelik/alüminyum konstrüksiyon, kompozit yüzey, ışıklı kasa seçenekleri.",
        "related_projects": ["volt-enerji", "kuzey-tekstil"],
        "related_services": ["tabela", "is-guvenligi-tabelalari", "kutu-harf", "display-pos"],
        "bilgi": ["/bilgi/totem-secim-rehberi/", "/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("Totem ile pylon farkı?", "Pylon genelde daha yüksek yol sistemi; aynı ailede ele alınır."),
            ("İzin gerekir mi?", "Konuma göre değişir; keşifte konuşulur."),
            ("Işıklı totem?", "Evet, gece yaklaşım için."),
            ("Temel kim yapar?", "Saha planına göre koordinasyon sağlanır."),
            ("Indoor totem?", "Display/POS sayfasına bakın."),
            ("OSB montajı?", "Evet, planlı keşif ile."),
            ("Süre?", "Temel ve üretime bağlıdır."),
            ("Bakım?", "Periyodik kontrol önerilir."),
        ],
    },
    "arac-giydirme": {
        "h1": "Araç Giydirme",
        "pk": "araç giydirme",
        "title": "Araç Giydirme | Filo ve Ticari Araç Kaplama",
        "desc": "Araç giydirme, filo kaplama ve ticari araç reklam uygulamaları.",
        "lede": "Filo ve ticari araçlarda tutarlı, dayanıklı giydirme uygulamaları.",
        "extra": [
            "Araç giydirme; baskılı folyonun araca uygulanmasıyla mobil marka yüzeyi oluşturur.",
            "Full wrap ve parça giydirme bu hizmetin alt uygulamalarıdır.",
            "Folyo baskı üretim adımıdır; sonuç ürün bu sayfada hedeflenir.",
            "Filo işlerinde şablon standardı ve araç tipi uyarlaması kritiktir.",
            "Tekirdağ geo: /hizmet-bolge/tekirdag-arac-giydirme/.",
        ],
        "apps": ["Panelvan", "Kurumsal filo", "Servis araçları", "Dağıtım", "Demo araçları"],
        "materials": "Araç folyoları, laminasyon (ihtiyaca göre), dijital baskı.",
        "related_projects": ["kuzey-tekstil"],
        "related_services": ["tabela", "cam-giydirme", "display-pos", "ofis-branding"],
        "bilgi": ["/bilgi/arac-giydirme-rehberi/"],
        "faqs": [
            ("Boya zarar görür mü?", "Doğru folyo ve uygulamada kontrollü söküm hedeflenir."),
            ("Full mu parça mı?", "Bütçe ve görünür alana göre."),
            ("Filo indirimi?", "Toplu işlerde kurumsal teklif hazırlanır."),
            ("Süre?", "Tek araçta genelde kısa; filoda planlı takvim."),
            ("Cam giydirme ayrı mı?", "Araç camı bu kapsamda; bina camı cam giydirme sayfasında."),
            ("Tasarım?", "Marka kılavuzuna göre uyarlanır."),
            ("Kışın uygulanır mı?", "Ortam sıcaklığı uygunluğu kontrol edilir."),
            ("Ömür?", "Folyo tipi ve kullanıma bağlıdır."),
        ],
    },
    "cam-giydirme": {
        "h1": "Cam Giydirme",
        "pk": "cam giydirme",
        "title": "Cam Giydirme | One Way Vision ve Vitrin Folyosu",
        "desc": "Cam giydirme, one way vision, vitrin ve cam folyo uygulamaları.",
        "lede": "Vitrin ve camda görünürlük, gizlilik ve mesaj dengesini kuran uygulamalar.",
        "extra": [
            "Cam giydirme; OWV, transparan/baskılı folyo ve vitrin grafiklerini kapsar.",
            "Window graphics / cam yazısı / vitrin reklamı aynı ailededir; ayrı URL yok.",
            "Ofis gizlilik paketi ofis branding ile birlikte yönetilebilir; malzeme bilgisi burada.",
            "Mağaza kampanyalarında hızlı yenileme avantajı sağlar.",
            "Tekirdağ geo: /hizmet-bolge/tekirdag-cam-giydirme/.",
        ],
        "apps": ["Mağaza vitrini", "Showroom", "Ofis cam bölme", "Kampanya dönemleri", "Giriş cephe camı"],
        "materials": "One way vision, transparan folyo, kumlama/frosted, baskılı vinil.",
        "related_projects": ["liman-kahve", "dortnal", "ekip-yazilim"],
        "related_services": ["isikli-tabela", "ofis-branding", "tabela", "display-pos"],
        "bilgi": ["/bilgi/one-way-vision-nedir/"],
        "faqs": [
            ("One way vision nedir?", "Dışarıdan grafik, içeriden görüş sağlayan delikli folyo."),
            ("İçerisi kararır mı?", "Folyo tipine göre ışık geçirgenliği değişir."),
            ("Araç camı?", "Araç giydirme kapsamında değerlendirilir."),
            ("Sökülür mü?", "Kampanya sonunda kontrollü söküm planlanır."),
            ("Buğu / yapışma?", "Cam hazırlığı ve uygulama kalitesi kritiktir."),
            ("Ofis paketi?", "Ofis branding sayfasına bakın."),
            ("Süre?", "Çoğu vitrin işi kısa sürer."),
            ("Tasarım?", "Mesaj hiyerarşisi okunur tutulur."),
        ],
    },
    "lightbox": {
        "h1": "Lightbox",
        "pk": "lightbox",
        "title": "Lightbox | Işıklı Kutu ve Backlit Frame",
        "desc": "Lightbox, ışıklı kutu, SEG ve backlit frame sistemleri.",
        "lede": "İnce kasa lightbox ve ışıklı kutu sistemleriyle premium aydınlatmalı görsel alanlar.",
        "extra": [
            "Lightbox; arkadan veya kenardan aydınlatmalı çerçeve sistemidir. Retail ve AVM’de sık tercih edilir.",
            "PK lock: ışıklı tabela / LED tabela → /hizmetler/isikli-tabela/. Bu sayfa lightbox ailesidir.",
            "SEG / backlit fabric hızlı görsel değişimi sağlar.",
            "Wave A2’de ayrı S×C yok; yerel talep city hub ve keşif ile yönetilir.",
            "Ofis ve resepsiyon duvarlarında lightbox + ofis branding birlikte planlanabilir.",
        ],
        "apps": ["Mağaza içi", "AVM", "Showroom", "Klinik bekleme", "Resepsiyon duvarı"],
        "materials": "Alüminyum kasa, LED, backlit fabric, SEG, akrilik yüz.",
        "related_projects": ["mera-otel", "dortnal", "ekip-yazilim"],
        "related_services": ["isikli-tabela", "display-pos", "ofis-branding", "cam-giydirme"],
        "bilgi": ["/bilgi/isikli-mi-isiksiz-mi/"],
        "faqs": [
            ("Işıklı tabeladan farkı?", "Cephe tabela ≠ lightbox kutu/frame."),
            ("SEG nedir?", "Silikon kenarlı kumaş germe sistem."),
            ("Görsel değişir mi?", "SEG’de hızlı değişim mümkündür."),
            ("İnce kasa?", "Mekâna göre kasa tipi seçilir."),
            ("Servis?", "LED ve kumaş değişimi planlanır."),
            ("Süre?", "Ölçü ve kasa tipine göre."),
            ("Fiyat?", "Ölçü + kasa + baskı."),
            ("Tekirdağ?", "Keşif üsten planlanır."),
        ],
    },
    "display-pos": {
        "h1": "Display & POS",
        "pk": "roll-up",
        "title": "Roll-Up, X-Banner ve POS Display",
        "desc": "Roll-up, X-banner, bayrak ve POS display sistemleri.",
        "lede": "Taşınabilir display ve POS: roll-up, X-banner, beach flag ve teşhir.",
        "extra": [
            "Display & POS taşınabilir donanım ailesidir. Roll-up birincil ticari başlıktır.",
            "Outdoor yol totemi /hizmetler/totem/ altındadır; karıştırılmaz.",
            "Tam fuar standı / backdrop sonraki fuar dalgasına aittir; tekil display burada.",
            "Mağaza içi kampanya ve etkinliklerde hızlı kurulum avantajı sağlar.",
            "Baskı + donanım birlikte teslim edilebilir.",
        ],
        "apps": ["Mağaza içi", "Etkinlik", "Bayi toplantısı", "Lansman", "Geçici yön noktası"],
        "materials": "Roll-up kasa, X-banner, beach flag, vinil/textile baskı, dekota tamamlayıcı.",
        "related_projects": ["dortnal", "liman-kahve"],
        "related_services": ["lightbox", "tabela", "cam-giydirme", "ofis-branding"],
        "bilgi": ["/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("Roll-up vs X-banner?", "Roll-up kasalı; X-banner daha ekonomik."),
            ("Fuar standı?", "Tekil display burada; tam stand ayrı hizmet dalgası."),
            ("Indoor totem?", "Bu ailede; yol totemi ayrı."),
            ("Adet avantajı?", "Toplu siparişte teklif özeldir."),
            ("Baskı kalitesi?", "Okunur mesafe ve çözünürlük planlanır."),
            ("Teslimat?", "Donanım + baskı birlikte."),
            ("Süre?", "Genelde kısa döngü."),
            ("Yeniden baskı?", "Aynı kasaya yeni baskı yapılabilir."),
        ],
    },
    "ofis-branding": {
        "h1": "Ofis Branding",
        "pk": "ofis branding",
        "title": "Ofis Branding | Resepsiyon ve Lobi Uygulamaları",
        "desc": "Ofis branding, resepsiyon, lobi ve kurumsal ofis grafikleri.",
        "lede": "Resepsiyon, lobi ve toplantı alanlarında kurumsal kimliğin mekâna uygulanması.",
        "extra": [
            "Ofis branding workplace kimlik paketidir: resepsiyon yazısı, logo duvarı, cam grafik, toplantı alanı.",
            "Genel duvar/zemin giydirme (her mekân) ayrı aile olarak ileride açılabilir; bu sayfa ofis paketini sahiplenır.",
            "Cam folyo uygulamaları cam giydirme uzmanlığıyla bağlanır.",
            "Plaza teslimatlarında mesaiye duyarlı montaj planlanır.",
            "Kutu harf / 3D logo sık tamamlayıcıdır.",
        ],
        "apps": ["Plaza ofisleri", "Resepsiyon", "Lobi", "Toplantı odası", "Kat kimliği"],
        "materials": "Kutu harf, cam folyo, duvar grafiği, kapı/oda isimliği (pakete göre).",
        "related_projects": ["ekip-yazilim", "mera-otel"],
        "related_services": ["kutu-harf", "cam-giydirme", "lightbox", "tabela"],
        "bilgi": ["/bilgi/kutu-harf-malzemeler/"],
        "faqs": [
            ("Kapı isimliği dahil mi?", "Pakete eklenebilir."),
            ("Cam giydirme ayrı mı?", "Malzeme/uygulama cam sayfasıyla; paket burada."),
            ("İç mekan giydirme farkı?", "Ofis = workplace paketi."),
            ("Kesinti olur mu?", "Mesai dışı planlanabilir."),
            ("Logo dosyası?", "Vektörel tercih edilir."),
            ("Süre?", "Alan büyüklüğüne göre."),
            ("Plaza yönetimi onayı?", "Gerekirse keşifte konuşulur."),
            ("Fiyat?", "Alan + malzeme + erişim."),
        ],
    },
    "is-guvenligi-tabelalari": {
        "h1": "İş Güvenliği Tabelaları",
        "pk": "iş güvenliği tabelaları",
        "title": "İş Güvenliği Tabelaları | Uyarı ve Acil Çıkış",
        "desc": "İSG tabelaları, uyarı levhaları, yangın çıkışı ve acil durum işaretleri.",
        "lede": "Fabrika, depo ve şantiyeler için uyarı, zorunlu işaret ve acil çıkış tabelaları.",
        "extra": [
            "İş güvenliği tabelaları statutory/uyarı setleridir. Yön bulma (oda/kat) wayfinding değildir.",
            "Yangın çıkışı, acil çıkış, toplanma alanı bu ailededir.",
            "Malt Studio üretim/tedarik yapar; belgelendirme kuruluşu değildir.",
            "OSB ve depolarda toplu saha etiketleme sık talep edilir.",
            "Reflektif seçenekler ihtiyaç halinde değerlendirilir.",
        ],
        "apps": ["Fabrika/OSB", "Depo", "Şantiye", "Ortak alan acil yön", "Üretim hattı uyarıları"],
        "materials": "Kompozit/forex, vinil, reflektif folyo (ihtiyaca göre).",
        "related_projects": ["volt-enerji", "kuzey-tekstil"],
        "related_services": ["tabela", "totem", "display-pos", "ofis-branding"],
        "bilgi": ["/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("Yangın çıkışı burada mı?", "Evet."),
            ("Yönlendirme aynı mı?", "Hayır; wayfinding ayrı aile."),
            ("ISO belgesi veriyor musunuz?", "Hayır; tabela üretiriz."),
            ("Toplu set?", "Listeye göre üretilir."),
            ("Dış mekân dayanım?", "Malzeme sahaya göre seçilir."),
            ("Montaj?", "Saha planıyla yapılır."),
            ("Süre?", "Standart setlerde hızlı."),
            ("Özel uyarı metni?", "Evet, onaya göre."),
        ],
    },
}


def service_process():
    return process_steps(
        [
            ("Keşif", "Ölçü, yüzey, erişim ve ihtiyaç netleştirilir."),
            ("Tasarım onayı", "Görsel ve teknik onay alınır."),
            ("Üretim", "Atölyede imalat ve kontrol."),
            ("Uygulama", "Saha montajı / giydirme."),
            ("Teslim", "Kontrol ve teslim notları."),
        ]
    )


def build_service(slug: str) -> None:
    s = SERVICE_DEPTH[slug]
    a5 = SERVICE_A5[slug]
    has_sxc = slug in A0
    canonical = f"{SITE}/hizmetler/{slug}/"
    ind_labels = {
        "fabrika-osb": "Fabrika & OSB",
        "restoran-cafe": "Restoran & Cafe",
        "saglik": "Sağlık",
        "plaza-ofis": "Plaza & Ofis",
        "insaat-santiye": "İnşaat & Şantiye",
        "perakende": "Perakende",
    }
    industries = [
        (f"/sektorler/{i}/", ind_labels.get(i, i), "Dikey giriş — money H1 değil.")
        for i in SERVICE_INDUSTRIES.get(slug, [])
    ]
    services = [
        (f"/hizmetler/{r}/", ALL_SERVICES[r], "İlgili hizmet — ayrı PK.")
        for r in s["related_services"]
        if r in ALL_SERVICES
    ]
    knowledge = [(b, "Rehber", "Eğitim — money H1 değil.") for b in s["bilgi"]]
    local_extra = ""
    if has_sxc:
        local_extra = block(
            "Tekirdağ yerel sahiplik",
            p(
                f"“Tekirdağ {s['h1']}” geo-money niyeti /hizmet-bolge/tekirdag-{slug}/ sayfasındadır.",
                "Bu sayfa coğrafyasız ticari niyeti taşır; iki URL aynı H1’i paylaşmaz.",
            ),
        )
    else:
        local_extra = block(
            "Yerel bağlantı",
            p(
                "Bu hizmet için ayrı Service×City URL’si yoktur (doorway üretilmez).",
                "Yerel keşif /bolgeler/tekirdag/ üzerinden planlanır.",
            ),
        )

    html = f"""{head(s["title"], s["desc"], canonical)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Hizmetler", "/hizmetler/"), (s["h1"], None))}
    <div class="eyebrow">Hizmet · Owner PK: {s["pk"]}</div>
    <h1>{s["h1"]}</h1>
    <p class="lede">{s["lede"]}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa(f"Merhaba, {s['h1']} hakkında teklif almak istiyorum.")}" target="_blank" rel="noopener">Teklif Al</a>
      <a class="btn btn-ghost" href="{wa(f"Merhaba, {s['h1']} hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Telefon · {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Bu hizmet nedir?", p(*s["extra"], *a5["intro"]) + f'<p class="note">Ownership: Birincil PK “{s["pk"]}”. Geo varyantlar S×C’de (varsa).</p>')}
    {block("Nerelerde kullanılır?", ul(s["apps"]) + p(*a5["where"]))}
    {block("Malzeme ve seçenekler", p(s["materials"], *a5["materials_extra"]))}
    {service_process()}
    {block("Süreç notları", p(*a5["process_extra"]))}
    {eeat_block("hizmet")}
    {block("Deneyim ve üretim", p(*a5["eeat"]))}
    {block("Fiyatı neler etkiler?", p(
        "Ölçü, malzeme, ışıklı/özel üretim, montaj yüksekliği, saha lojistiği ve adet fiyatı belirler.",
        "Sabit internet fiyat listesi yayınlanmaz; keşif sonrası net teklif verilir.",
        "Faktör eğitimi için /bilgi/tabela-fiyati/ rehberine bakabilirsiniz.",
    ))}
    {block("Süre ve planlama", p(
        "Tasarım onayı sonrası süre işin ölçeğine göre değişir.",
        "Acil işler operasyon kapasitesine göre değerlendirilir; garanti edilemeyen vaat verilmez.",
    ))}
    {block("Bakım ve sonrası", p(*a5["maintenance"]))}
    {block("Uygulama notları", p(*SERVICE_EXPAND[slug], *SERVICE_EXPAND2[slug]))}
    {block("Karar ve teslim özeti", p(
        SERVICE_LONG[slug],
        SERVICE_LONG2[slug],
        *([SERVICE_BRIDGE[slug]] if slug in SERVICE_BRIDGE else []),
        *([SERVICE_NUDGE[slug]] if slug in SERVICE_NUDGE else []),
    ))}
    {block("Keşif kontrol listesi", ul(SERVICE_CHECKLIST[slug]))}
    {local_extra}
    {mid_cta(f"Merhaba, {s['h1']} için keşif istiyorum.")}
  </div>
</section>
{related_rail(
    services=services,
    knowledge=knowledge,
    projects=s["related_projects"],
    industries=industries,
)}
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Sık sorulan sorular</h2>
    <div class="faq">{faq_html(s["faqs"])}</div>
  </div>
</section>
{cta_band(f"{s['h1']} için teklif alın", f"Merhaba, {s['h1']} teklifi istiyorum.")}
{footer()}
</body></html>
"""
    write(ROOT / "hizmetler" / slug / "index.html", html)


def build_sxc(slug: str) -> None:
    s = SERVICE_DEPTH[slug]
    name = s["h1"]
    canonical = f"{SITE}/hizmet-bolge/tekirdag-{slug}/"
    # Unique local paragraphs per service
    local = {
        "tabela": "Tekirdağ merkez ve Süleymanpaşa çarşı aksında mağaza tabela talepleri yoğundur. OSB koridoruna giden işler Tekirdağ üssünden planlanır; Çorlu/Çerkezköy için ayrı city URL’leri sonraki dalgadadır.",
        "isikli-tabela": "Tekirdağ’da gece açık kalan ticaret ve plaza cephelerinde LED ışıklı tabela sık istenir. Lightbox ihtiyacı ayrıca ayrılır.",
        "kutu-harf": "Tekirdağ plaza ve ofis cephelerinde kutu harf, prestij algısını hızlı yükseltir. Channel letters aynı ailede değerlendirilir.",
        "totem": "Tesis girişi ve yol yaklaşımında totem, Tekirdağ çevre sanayi taleplerinde öne çıkar. Temel/montaj keşifle planlanır.",
        "arac-giydirme": "Tekirdağ merkezli filolar ve ticari araçlar için giydirme, lojistik görünürlüğü artırır.",
        "cam-giydirme": "Tekirdağ mağaza vitrinlerinde OWV ve kampanya folyosu hızlı yenilenebilir yüzey sağlar.",
    }[slug]
    faqs = [
        (f"Tekirdağ’da {name.lower()} yaptırabilir miyim?", "Evet. Bu sayfa yerel ticari niyetin birincil sahibidir."),
        ("Genel hizmet sayfasından farkı?", f"Genel sayfa “{s['pk']}” niyetini; bu sayfa “tekirdağ {s['pk']}” niyetini taşır."),
        ("Süleymanpaşa ayrı mı?", "Hayır; Tekirdağ S×C ve city hub’a alias bağlanır."),
        ("Fiyat?", "Yerel erişim + ölçü/malzeme/montaj keşifle netleşir."),
        ("Keşif?", "Tekirdağ üssünden planlanır."),
        ("Proje örneği?", "İlgili proje sayfalarına bakın; görseller eklendikçe güçlenir."),
    ]
    others = cards(
        [
            (f"/hizmet-bolge/tekirdag-{o}/", f"Tekirdağ {A0[o]}", "İlgili yerel sayfa.", "S×C")
            for o in A0
            if o != slug
        ][:5]
    )
    html = f"""{head(f"Tekirdağ {name} | Yerel Üretim ve Montaj", f"Tekirdağ {name.lower()} üretimi ve montajı. {s['desc']}", canonical)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Hizmetler","/hizmetler/"),(name,f"/hizmetler/{slug}/"),(f"Tekirdağ {name}",None))}
    <div class="eyebrow">Service × City · Geo-money owner</div>
    <h1>Tekirdağ {name}</h1>
    <p class="lede">{local}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa(f"Merhaba, Tekirdağ {name} teklifi istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara</a>
      <a class="btn btn-ghost" href="/hizmetler/{slug}/">{name} (genel)</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block(f"Tekirdağ’da {name.lower()}", p(
        local,
        s["extra"][0],
        s["extra"][1] if len(s["extra"])>1 else "",
        "Anti-doorway: Bu sayfa ebeveyn hizmetin kopyası değildir. Yerel operasyon, talep bağlamı ve Tekirdağ lojistiği eklenmiştir.",
        "Süleymanpaşa / merkez talepleri bu URL ve Tekirdağ city hub altında toplanır.",
    ))}
    {block("Yerel uygulamalar", ul(s["apps"]) + p(*SERVICE_A5[slug]["where"]))}
    {block("Üretim ve montaj lojistiği", p(
        s["extra"][2] if len(s["extra"])>2 else s["extra"][0],
        "Keşif, üretim ve saha montajı Tekirdağ üssünden koordine edilir. Çevre ilçe ve OSB sahalarında lojistik teklife yansır.",
        "Montaj penceresi işletme saatleri ve saha erişimine göre planlanır.",
        *SERVICE_A5[slug]["process_extra"],
    ))}
    {service_process()}
    {eeat_block("yerel hizmet")}
    {block("Yerel fiyat faktörleri", p(
        s["materials"],
        "Tekirdağ içi erişim genelde standarttır; vinç, yükseklik, izin ve OSB girişi ek maliyet doğurabilir.",
        "Net rakam keşif sonrası verilir.",
    ))}
    {block("Bakım (yerel)", p(*SERVICE_A5[slug]["maintenance"]))}
    {mid_cta(f"Tekirdağ {name} keşif")}
  </div>
</section>
{related_rail(
    services=[
        (f"/hizmetler/{slug}/", name, "Non-geo parent owner."),
        *[(f"/hizmetler/{r}/", ALL_SERVICES[r], "İlgili hizmet.") for r in s["related_services"] if r in ALL_SERVICES][:3],
    ],
    knowledge=[(b, "Rehber", "Eğitim.") for b in s["bilgi"]],
    projects=s["related_projects"],
    industries=[
        (f"/sektorler/{i}/", {"fabrika-osb":"Fabrika & OSB","restoran-cafe":"Restoran & Cafe","saglik":"Sağlık","plaza-ofis":"Plaza & Ofis","insaat-santiye":"İnşaat & Şantiye","perakende":"Perakende"}.get(i,i), "Dikey.")
        for i in SERVICE_INDUSTRIES.get(slug, [])[:2]
    ],
    hubs=[
        ("/bolgeler/tekirdag/", "Tekirdağ", "City hub"),
        ("/hizmetler/", "Hizmetler", "Hub"),
        ("/projeler/", "Projeler", "Kanıt"),
        ("/", "Ana sayfa", "Authority"),
    ],
)}
<section class="section-band">
  <div class="wrap">
    <h2>İlgili Tekirdağ sayfaları</h2>
    <div class="card-grid">{others}</div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Sık sorulan sorular</h2>
    <div class="faq">{faq_html(faqs)}</div>
  </div>
</section>
{cta_band(f"Tekirdağ {name} teklifi", f"Tekirdağ {name} teklifi")}
{footer()}
</body></html>
"""
    write(ROOT / "hizmet-bolge" / f"tekirdag-{slug}" / "index.html", html)


def build_city() -> None:
    canonical = f"{SITE}/bolgeler/tekirdag/"
    svc = cards([(f"/hizmetler/{s}/", n, "Non-geo hizmet.", "Hizmet") for s, n in ALL_SERVICES.items()])
    sxc = cards([(f"/hizmet-bolge/tekirdag-{s}/", f"Tekirdağ {n}", "Geo-money owner.", "S×C") for s, n in A0.items()])
    faqs = [
        ("Tekirdağ’da tabela / reklam firması mısınız?", "Evet. Malt Studio Tekirdağ merkezlidir."),
        ("Süleymanpaşa sayfası?", "Ayrı URL yok; bu hub ve Tekirdağ S×C’ye bağlanır."),
        ("Çorlu / Çerkezköy?", "Ayrı city URL’leri sonraki dalgada; keşif bugün Tekirdağ üssünden."),
        ("Hangi hizmetler?", "A0 + A2 hizmet listesine bakın."),
        ("Proje var mı?", "/projeler/ altında vaka sayfaları vardır."),
        ("Keşif?", "WhatsApp veya telefon ile randevu."),
    ]
    html = f"""{head("Tekirdağ Reklam ve Tabela | Yerel Hizmet Rehberi", "Tekirdağ reklam firması ve tabela üreticisi Malt Studio. Yerel hizmetler ve iletişim.", canonical)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Tekirdağ",None))}
    <div class="eyebrow">City hub · Local / firm owner</div>
    <h1>Tekirdağ Reklam Ajansı &amp; Üretici</h1>
    <p class="lede">Tekirdağ’da üreten ve uygulayan ekip. Bu sayfa yerel firma niyetini taşır; “Tekirdağ + hizmet” geo-money H1’lerini S×C sayfalarına bırakır.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa("Tekirdağ keşif")}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara</a>
      <a class="btn btn-ghost" href="/hizmetler/">Hizmetler</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Tekirdağ’da ne sunuyoruz?", p(
        "Malt Studio; tabela, ışıklı tabela, kutu harf, totem, araç giydirme, cam giydirme ile lightbox, display/POS, ofis branding ve iş güvenliği tabelaları üretir.",
        "Merkez Tekirdağ’dır. Süleymanpaşa / merkez aramaları bu hub ve ilgili S×C sayfalarına yönlenir — paralel ilçe ağacı açılmaz.",
        "Sanayi koridoru (Çorlu, Çerkezköy, Kapaklı, Ergene) talepleri operasyonel olarak üsten yönetilir; ayrı city sayfaları yayınlandıkça bağlanacaktır.",
        "Yerel güven için proje sayfaları ve saha görselleri kritiktir. Görseller onaylandıkça proje URL’lerine eklenir.",
    ))}
    {block("Yerel nasıl çalışırız?", p(
        "Keşif randevusu → ölçü → tasarım onayı → atölye üretimi → saha montajı.",
        "Mağaza, plaza, fabrika ve ofis işlerinde montaj penceresi işletmeye göre ayarlanır.",
        "Acil montaj/tamir talepleri kapasiteye göre değerlendirilir; tutulmayan süre vaadi verilmez.",
    ))}
    {eeat_block("şehir")}
    {block("Süleymanpaşa alias politikası", p(
        "Süleymanpaşa için ayrı Service×City ağacı oluşturulmaz. Bu, cannibalization ve doorway riskini önlemek içindir.",
        "İçerikte merkez / Süleymanpaşa doğal dilde anılır; kanonik coğrafi owner Tekirdağ’dır.",
    ))}
    {block("Yerel talep senaryoları", ul([
        "Çarşı / mağaza: tabela + ışıklı + cam giydirme",
        "OSB / fabrika: totem + tabela + İSG + filo",
        "Plaza / ofis: kutu harf + ofis branding",
        "Perakende açılış: ışıklı + vitrin paketi",
    ]))}
    {block("İletişim ve keşif", p(
        "WhatsApp veya telefon ile kısa brief bırakın; uygunsa keşif planlanır.",
        "Geo-money (“Tekirdağ + hizmet”) için aşağıdaki S×C kartlarını kullanın.",
    ))}
  </div>
</section>
{related_rail(
    services=[(f"/hizmetler/{s}/", n, "Hizmet owner.") for s, n in list(A0.items())[:6]],
    knowledge=[(f"/bilgi/{s}/", t, "Rehber.") for s, t, _, _ in ARTICLES[:4]],
    projects=["liman-kahve","volt-enerji","dortnal","mera-otel","ekip-yazilim","kuzey-tekstil"],
    industries=[(f"/sektorler/{s}/", n, "Dikey.") for s, n, _ in INDUSTRIES[:4]],
)}
<section class="section-band">
  <div class="wrap">
    <h2>Tekirdağ hizmet × şehir</h2>
    <p class="intro">“Tekirdağ + hizmet” aramalarının sahibi bu S×C sayfalarıdır.</p>
    <div class="card-grid">{sxc}</div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Tüm hizmetler</h2>
    <div class="card-grid">{svc}</div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>Sektörler ve bilgi</h2>
    <div class="card-grid">{cards([
        ("/sektorler/", "Sektörler", "Fabrika, restoran, sağlık…", "A1"),
        ("/bilgi/", "Bilgi", "Rehberler ve karşılaştırmalar.", "A1"),
        ("/projeler/", "Projeler", "Vaka kanıtı.", "A1"),
    ])}</div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Sık sorulan sorular</h2>
    <div class="faq">{faq_html(faqs)}</div>
  </div>
</section>
{cta_band("Tekirdağ’da keşif veya teklif", "Tekirdağ keşif")}
{footer()}
</body></html>
"""
    write(ROOT / "bolgeler" / "tekirdag" / "index.html", html)


def build_hizmetler_hub() -> None:
    a0 = cards([(f"/hizmetler/{s}/", n, "Çekirdek hizmet.", "A0") for s, n in A0.items()])
    a2 = cards([(f"/hizmetler/{s}/", n, "A2 hizmet.", "A2") for s, n in A2.items()])
    sxc = cards([(f"/hizmet-bolge/tekirdag-{s}/", f"Tekirdağ {n}", "Geo-money.", "S×C") for s, n in A0.items()])
    html = f"""{head("Hizmetler | Tabela, Lightbox, Ofis Branding ve Daha Fazlası", "Malt Studio tüm hizmetleri: tabela, ışıklı tabela, kutu harf, totem, araç ve cam giydirme, lightbox, display, ofis branding, İSG.", f"{SITE}/hizmetler/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Hizmetler",None))}
    <div class="eyebrow">Hizmet hub</div>
    <h1>Hizmetler</h1>
    <p class="lede">Her hizmetin tek sahibi URL’si vardır. Geo-money sayfalar S×C altındadır.</p>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Nasıl seçmelisiniz?", p(
        "Önce ihtiyacı netleştirin: cephe tabela, ışıklı sistem, kutu harf, araç, cam, lightbox, display veya ofis paketi.",
        "Kararsızsanız rehberleri (/bilgi/) okuyun veya WhatsApp ile kısa keşif isteyin.",
        "Tekirdağ + hizmet arıyorsanız aşağıdaki S×C kartlarına gidin.",
    ))}
    {eeat_block("hizmet hub")}
  </div>
</section>
{related_rail(
    knowledge=[(f"/bilgi/{s}/", t, "Rehber.") for s, t, _, _ in ARTICLES[:4]],
    projects=["liman-kahve", "dortnal", "volt-enerji"],
    industries=[(f"/sektorler/{s}/", n, "Dikey.") for s, n, _ in INDUSTRIES[:4]],
)}
<section class="section-band paper-band">
  <div class="wrap"><h2>Çekirdek hizmetler (A0)</h2><div class="card-grid">{a0}</div></div>
</section>
<section class="section-band">
  <div class="wrap"><h2>Wave A2 hizmetler</h2><div class="card-grid">{a2}</div></div>
</section>
<section class="section-band paper-band">
  <div class="wrap"><h2>Tekirdağ yerel sayfalar</h2><div class="card-grid">{sxc}</div></div>
</section>
{cta_band("Hangi hizmet size uygun?", "Hizmet seçimi için yardımcı olur musunuz?")}
{footer()}
</body></html>
"""
    write(ROOT / "hizmetler" / "index.html", html)


def _knowledge_for(services: list[str]) -> list[tuple[str, str]]:
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for s in services:
        for href, label in KNOWLEDGE_BY_SERVICE.get(s, []):
            if href not in seen:
                seen.add(href)
                out.append((href, label))
    return out[:4]


def build_project(slug: str, name: str, industry: str, services: list[str]) -> None:
    """Wave A4 case-study template. noindex until real evidence exists."""
    case = CASES.get(slug)
    if not case:
        raise SystemExit(f"A4 case seed missing for {slug}")
    name = case["name"]
    industry = case["industry"]
    services = case["services"]
    ind_label = INDUSTRY_LABEL.get(industry, industry)
    canonical = f"{SITE}/projeler/{slug}/"
    noindex = True  # EEAT gate — do not remove until real photos exist

    svc_cards = cards(
        [
            (f"/hizmetler/{s}/", ALL_SERVICES[s], f"{name} kapsamında aday hizmet.", "Hizmet")
            for s in services
            if s in ALL_SERVICES
        ]
    )
    bil_cards = cards(
        [(href, label, "İlgili rehber — money H1 taşımaz.", "Bilgi") for href, label in _knowledge_for(services)]
    )
    rel = case["related_projects"]
    rel_cards = cards(
        [
            (
                f"/projeler/{s}/",
                CASES[s]["name"] if s in CASES else s,
                "İlgili vaka — kanıt kapısı açık.",
                "Proje",
            )
            for s in rel
            if s != slug
        ]
    )

    meta = f"""<dl class="case-meta">
  <div><dt>Proje</dt><dd>{name}</dd></div>
  <div><dt>Konum</dt><dd><a href="/bolgeler/tekirdag/">Tekirdağ</a></dd></div>
  <div><dt>Sektör</dt><dd><a href="/sektorler/{industry}/">{ind_label}</a></dd></div>
  <div><dt>Index durumu</dt><dd>noindex,follow — görsel kanıt kapısı</dd></div>
</dl>"""

    applied = "<ul class='scope-list'>" + "".join(
        f"<li><a href='/hizmetler/{s}/'>{ALL_SERVICES[s]}</a> — kapsam adayı; kesin kalem onaylı iş emrine bağlı.</li>"
        for s in services
        if s in ALL_SERVICES
    ) + "</ul>"

    order = [s for s, *_ in PROJECTS]
    idx = order.index(slug)
    prev_s = order[(idx - 1) % len(order)]
    next_s = order[(idx + 1) % len(order)]
    prev_n = CASES[prev_s]["name"]
    next_n = CASES[next_s]["name"]
    nav = f"""<nav class="case-nav" aria-label="Proje gezintisi">
  <a class="btn btn-ghost" href="/projeler/{prev_s}/">← {prev_n}</a>
  <a class="btn btn-ghost" href="/projeler/">Tüm projeler</a>
  <a class="btn btn-ghost" href="/projeler/{next_s}/">{next_n} →</a>
</nav>"""

    html = f"""{head(case["title"], case["desc"], canonical, noindex=noindex)}
<body>
{header()}
<article class="case-study" data-project="{slug}">
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Projeler","/projeler/"),(name,None))}
    <div class="eyebrow">Case study · EEAT proof node</div>
    <h1>{case["h1"]}</h1>
    <p class="lede">{case["lede"]}</p>
    {meta}
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa(f"Merhaba, {name} benzeri proje için teklif almak istiyorum.")}" target="_blank" rel="noopener">Teklif Al</a>
      <a class="btn btn-ghost" href="{wa(f"{name} benzeri proje")}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Telefon</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Proje özeti", p(*case["summary"]))}
    {block("Müşteri ihtiyacı", p(*case["need"]))}
    {block("İş kapsamı", p(*case["scope"]))}
    {block("Uygulanan hizmetler", applied + p("Hizmet sayfaları ticari niyeti taşır; bu sayfa kanıt düğümüdür."))}
    {block("Üretim süreci", p(*case["process"]))}
    {block("Montaj / uygulama", p(*case["installation"]))}
    {block("Kullanılan malzemeler", p(*case["materials"]))}
    {block("Teknik detaylar", p(*case["technical"]))}
    {block("Sonuç", p(*case["result"]))}
    <div class="content-block">
      <h2>EEAT durumu</h2>
      <p class="awaiting">Gerçek galeri, before/after, montaj, atölye ve malzeme close-up fotoğrafları onaylanana kadar bu vaka indekslenmez (noindex,follow). Uydurma görsel veya uydurma metrik eklenmez.</p>
      <ul>
        <li>Atölye üretimi ve saha montajı aynı operasyonel hat üzerinden planlanır.</li>
        <li>Yayın öncesi müşteri onayı zorunludur.</li>
        <li>Kanıt slotları aşağıda hazırdır; <code>&lt;img&gt;</code> eklenince figcaption korunur.</li>
      </ul>
    </div>
  </div>
</section>
{evidence_gallery(name)}
<section class="section-band paper-band" aria-labelledby="applied-services-title">
  <div class="wrap">
    <h2 id="applied-services-title">İlgili hizmetler</h2>
    <p class="intro">Bu vakada adı geçen hizmetlerin sahiplik sayfaları.</p>
    <div class="card-grid">{svc_cards}</div>
  </div>
</section>
<section class="section-band" aria-labelledby="related-industry-title">
  <div class="wrap">
    <h2 id="related-industry-title">İlgili sektör</h2>
    <div class="card-grid">{cards([
        (f"/sektorler/{industry}/", ind_label, "Dikey bağlam sayfası.", "Sektör"),
        ("/bolgeler/tekirdag/", "Tekirdağ", "Yerel firma / city hub.", "City"),
        ("/projeler/", "Tüm projeler", "Kanıt indeksi.", "Hub"),
    ])}</div>
  </div>
</section>
<section class="section-band paper-band" aria-labelledby="related-knowledge-title">
  <div class="wrap">
    <h2 id="related-knowledge-title">İlgili rehberler</h2>
    <p class="intro">Eğitim içerikleri. Money keyword sahipliği hizmet sayfalarındadır.</p>
    <div class="card-grid">{bil_cards}</div>
  </div>
</section>
<section class="section-band" aria-labelledby="related-projects-title">
  <div class="wrap">
    <h2 id="related-projects-title">İlgili projeler</h2>
    <div class="card-grid">{rel_cards}</div>
    <div style="margin-top:32px;display:flex;gap:12px;flex-wrap:wrap;justify-content:space-between;">{nav}</div>
  </div>
</section>
{related_rail(hubs=[
    ("/projeler/", "Projeler", "Kanıt hub"),
    ("/hizmetler/", "Hizmetler", "Hizmet hub"),
    ("/bilgi/", "Bilgi", "Rehber hub"),
    ("/sektorler/", "Sektörler", "Dikey hub"),
    ("/bolgeler/tekirdag/", "Tekirdağ", "City hub"),
    ("/", "Ana sayfa", "Authority"),
])}
{project_cta(name)}
</article>
{footer()}
</body></html>
"""
    write(ROOT / "projeler" / slug / "index.html", html)


def build_projeler_hub() -> None:
    items = cards([(f"/projeler/{s}/", n, "Vaka — görsel kapısı açık.", "Proje") for s, n, _, _ in PROJECTS])
    html = f"""{head("Projeler | Malt Studio İş Örnekleri", "Tabela, ışıklı tabela, kutu harf ve giydirme proje örnekleri.", f"{SITE}/projeler/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Projeler",None))}
    <div class="eyebrow">Proof layer</div>
    <h1>Projeler</h1>
    <p class="lede">Kanıt düğümleri. Money H1 taşımaz; hizmet ve şehir sayfalarına otorite aktarır.</p>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Neden proje sayfaları?", p(
        "Google ve kullanıcılar gerçek iş ister. Proje sayfaları benzersiz kanıttır.",
        "Görseller onaylanana kadar tekil proje URL’leri noindex,follow olabilir.",
        "Hub indexlenebilir; listelemeyi ve iç link akışını taşır.",
    ))}
    {eeat_block("proje hub")}
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap"><h2>Vakalar</h2><div class="card-grid">{items}</div></div>
</section>
{related_rail(
    services=[(f"/hizmetler/{s}/", n, "Hizmet owner.") for s, n in list(A0.items())[:6]],
    knowledge=[(f"/bilgi/{s}/", t, "Rehber.") for s, t, _, _ in ARTICLES[:3]],
    industries=[(f"/sektorler/{s}/", n, "Dikey.") for s, n, _ in INDUSTRIES[:4]],
)}
{cta_band("Projenizi konuşalım", "Yeni proje")}
{footer()}
</body></html>
"""
    write(ROOT / "projeler" / "index.html", html)


INDUSTRY_COPY = {
    "fabrika-osb": (
        "Sanayi tesislerinde tabela; kimlik, yön ve dayanımdır.",
        ["Tesis totemi", "Cephe yazısı", "İSG levhaları", "Filo giydirme", "Saha yön tabelaları"],
        ["totem", "tabela", "kutu-harf", "arac-giydirme", "is-guvenligi-tabelalari"],
        ["volt-enerji", "kuzey-tekstil"],
    ),
    "restoran-cafe": (
        "F&B’de tabela ve vitrin ilk karar anını yönetir.",
        ["Işıklı cephe", "Vitrin giydirme", "Gece okunurluk", "Kampanya yüzeyleri"],
        ["isikli-tabela", "cam-giydirme", "tabela", "lightbox"],
        ["liman-kahve"],
    ),
    "saglik": (
        "Sağlık noktalarında sakin, okunur ve güven veren görünürlük gerekir.",
        ["Kurumsal ışıklı tabela", "İç yön tabelaları", "Cam grafik", "Sade dil"],
        ["isikli-tabela", "tabela", "cam-giydirme", "ofis-branding"],
        [],
    ),
    "plaza-ofis": (
        "Plaza ve ofiste ilk izlenim resepsiyon ve cephede kurulur.",
        ["Kutu harf", "Ofis branding", "Cam folyo", "Lightbox"],
        ["kutu-harf", "ofis-branding", "cam-giydirme", "lightbox", "tabela"],
        ["mera-otel", "ekip-yazilim"],
    ),
    "insaat-santiye": (
        "Şantiye çevresinde proje mesajı ve saha görünürlüğü gerekir.",
        ["Proje panoları", "Geçici yön", "Uyarı yüzeyleri", "Hızlı üretim"],
        ["tabela", "totem", "display-pos", "is-guvenligi-tabelalari"],
        [],
    ),
    "perakende": (
        "Mağaza cephesi satışa açılan vitrindir.",
        ["Işıklı mağaza tabela", "OWV / vitrin", "Kampanya yenileme", "Açılış paketi"],
        ["isikli-tabela", "cam-giydirme", "tabela", "display-pos", "lightbox"],
        ["dortnal", "liman-kahve"],
    ),
}


def build_industry(slug: str, name: str, pk: str) -> None:
    lede, needs, services, projs = INDUSTRY_COPY[slug]
    a5 = INDUSTRY_A5[slug]
    svc_links = [
        (f"/hizmetler/{s}/", ALL_SERVICES[s], "Önerilen hizmet owner.")
        for s in services
        if s in ALL_SERVICES
    ]
    bil_links = [(h, "Rehber", "Eğitim — money H1 değil.") for h in a5["knowledge"]]
    html = f"""{head(f"{name} Tabela ve Görünürlük Çözümleri", f"{name} sektörü için tabela ve görünürlük. Malt Studio.", f"{SITE}/sektorler/{slug}/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Sektörler","/sektorler/"),(name,None))}
    <div class="eyebrow">Industry · PK: {pk}</div>
    <h1>{name}</h1>
    <p class="lede">{lede}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa(f"{name} sektörü keşif")}" target="_blank" rel="noopener">Teklif Al</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Telefon</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Sektör ihtiyacı", p(
        lede,
        "Bu sayfa dikey giriştir; bare service money PK taşımaz. Satın alma ilgili hizmet URL’lerindedir.",
        "Tekirdağ üssünden keşif yapılır; koridor ilçeleri operasyonel kapsamda değerlendirilir.",
    ))}
    {block("Sık karşılaşılan sorunlar", ul(a5["problems"]))}
    {block("Tipik ihtiyaçlar", ul(needs))}
    {block("Önerilen hizmet seti", p(
        "Aşağıdaki hizmetler bu dikeyde sık bir araya gelir. Her biri kendi owner URL’sine sahiptir.",
    ) + ul([ALL_SERVICES[s] for s in services if s in ALL_SERVICES]))}
    {block("Proje iş akışı", p(*a5["workflow"]))}
    {block("Malzeme önerileri", p(*a5["materials"]))}
    {block("Bakım ve saha notları", p(*a5["maintenance"]))}
    {block("Saha pratikleri", p(*INDUSTRY_EXPAND[slug], INDUSTRY_LONG[slug], INDUSTRY_BRIDGE[slug]))}
    {eeat_block("sektör")}
    {mid_cta(f"{name} sektörü keşif")}
  </div>
</section>
{related_rail(services=svc_links, knowledge=bil_links, projects=projs or ["liman-kahve", "volt-enerji"])}
<section class="section-band paper-band">
  <div class="wrap"><h2>SSS</h2><div class="faq">{faq_html([
      (f"{name} için hangi hizmetler?", ", ".join(ALL_SERVICES[s] for s in services if s in ALL_SERVICES)+"."),
      ("Bu hizmet sayfasının yerine geçer mi?", "Hayır; dikey girişidir."),
      ("Tekirdağ’da uygulanır mı?", "Evet; keşif city hub üzerinden planlanır."),
      ("Teklif?", "WhatsApp veya telefon ile keşif talebi bırakın."),
  ])}</div></div>
</section>
{cta_band(f"{name} için keşif", f"{name} keşif")}
{footer()}
</body></html>
"""
    write(ROOT / "sektorler" / slug / "index.html", html)


def build_sektorler_hub() -> None:
    items = cards([(f"/sektorler/{s}/", n, f"PK: {pk}", "Sektör") for s, n, pk in INDUSTRIES])
    html = f"""{head("Sektörler | Fabrika, Restoran, Sağlık, Plaza", "Sektörel tabela ve görünürlük çözümleri.", f"{SITE}/sektorler/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Sektörler",None))}
    <h1>Sektörler</h1>
    <p class="lede">Dikey girişler. Hizmet PK’sini çalmaz; A0/A2 hizmetlere bağlar.</p>
  </div>
</section>
<section class="page-main"><div class="wrap">{block("Nasıl kullanılır?", p("Sektörünüzü seçin, ilgili hizmetlere ve projelere geçin.","Kararsızsanız Tekirdağ hub veya WhatsApp ile yazın."))}{eeat_block("sektör hub")}</div></section>
<section class="section-band paper-band"><div class="wrap"><div class="card-grid">{items}</div></div></section>
{related_rail(
    services=[(f"/hizmetler/{s}/", n, "Hizmet.") for s, n in list(A0.items())[:6]],
    knowledge=[(f"/bilgi/{s}/", t, "Rehber.") for s, t, _, _ in ARTICLES[:3]],
    projects=["liman-kahve", "volt-enerji", "dortnal"],
)}
{cta_band("Sektörünüze uygun çözüm", "Sektör keşfi")}
{footer()}
</body></html>
"""
    write(ROOT / "sektorler" / "index.html", html)


ARTICLE_BODY = {
    "tabela-cesitleri": [
        ("Giriş", "Tabela seçimi estetik kadar okunurluk, dayanım ve montaj koşullarının toplamıdır. Bu rehber bilgilendirme amaçlıdır; satın alma /hizmetler/tabela/ sayfasındadır."),
        ("Işıksız tabela", "Gündüz odaklı, genelde daha ekonomik cephe çözümleridir. Gece ihtiyacı yoksa doğru tercihtir."),
        ("Işıklı tabela", "Gece görünürlük gereken noktalarda LED’li sistemler kullanılır. Ayrı hizmet sayfası vardır."),
        ("Kutu harf", "Üç boyutlu cephe yazısıdır; prestij ve derinlik sağlar."),
        ("Totem", "Yol ve tesis yaklaşımında uzaktan algı için dikey sistemlerdir."),
        ("Cam giydirme", "Vitrin mesajı ve gizlilik/görünürlük dengesi için folyo uygulamalarıdır."),
        ("Lightbox", "İç mekân/retail ışıklı kutu sistemidir; ışıklı tabela ile karıştırılmamalıdır."),
        ("Seçim çerçevesi", "Konum, gece ihtiyacı, bütçe, izin ve montaj yüzeyi birlikte değerlendirilir."),
    ],
    "isikli-mi-isiksiz-mi": [
        ("Karar sorusu", "İşletmeniz gece de görünmek zorunda mı? Bu soru çoğu tercihi belirler."),
        ("Görünürlük", "Işıklı gece avantajı sağlar; ışıksız gündüz yeterli olabilir."),
        ("Maliyet", "Işıklıda kasa, LED ve elektrik maliyeti eklenir."),
        ("Bakım", "LED ve güç kaynakları servis gerektirebilir."),
        ("Cephe ve izin", "Mimari ve elektrik altyapısı seçimi etkiler."),
        ("Lightbox ayrımı", "Lightbox ayrı üründür; cephe ışıklı tabela değildir."),
        ("Sonuç", "Ticari uygulama için /hizmetler/isikli-tabela/ veya tabela sayfasına geçin."),
    ],
    "kutu-harf-malzemeler": [
        ("Amaç", "Malzeme karşılaştırması bilgilendirmedir. Satın alma /hizmetler/kutu-harf/ altındadır."),
        ("Pleksi / akrilik", "Işıklı harflerde yaygın; renk ve ışık geçirgenliği avantajlıdır."),
        ("Paslanmaz", "Prestij ve dış dayanım; bütçe daha yüksek olabilir."),
        ("Işıklı vs ışıksız", "Gece okunurluk ihtiyacına göre karar verilir."),
        ("Montaj yüzeyi", "Kompozit, beton, cam — keşif şarttır."),
        ("Channel letters", "Aynı ailedir; ayrı URL yoktur."),
        ("Bakım", "Dış ortamda periyodik kontrol önerilir."),
    ],
    "one-way-vision-nedir": [
        ("Tanım", "One way vision; dışarıdan grafik görünen, içeriden bakışa izin veren delikli folyodur."),
        ("Kullanım", "Mağaza vitrini, showroom, uygun araç camı uygulamaları."),
        ("Alternatifler", "Transparan baskı, kumlama folyo, opak folyo."),
        ("Işık ve görüş", "Delik oranı içerisi aydınlığını etkiler."),
        ("Uygulama", "Cam temizliği ve doğru gergi kritiktir."),
        ("Ticari sayfa", "Uygulama /hizmetler/cam-giydirme/ altındadır."),
    ],
    "arac-giydirme-rehberi": [
        ("Süreç", "Ölçü → tasarım → baskı → yüzey hazırlığı → uygulama."),
        ("Full vs parça", "Bütçe ve marka alanına göre seçilir."),
        ("Filo", "Şablon standardı + araç tipi uyarlaması."),
        ("Ömür", "Folyo tipi, yıkama, güneş ve kullanım."),
        ("Söküm", "Doğru folyo ile kontrollü söküm hedeflenir."),
        ("Ticari sayfa", "/hizmetler/arac-giydirme/ ve Tekirdağ S×C."),
    ],
    "tabela-fiyati": [
        ("Uyarı", "Bu sayfa fiyat eğitimidir; sabit fiyat listesi değildir. Geo fiyat niyeti S×C fiyat modüllerine aittir."),
        ("Ölçü", "m² ve harf yüksekliği temel çarpandır."),
        ("Malzeme", "Kompozit, pleksi, paslanmaz farklı maliyetler."),
        ("Işık", "LED, trafo, kasa derinliği."),
        ("Montaj", "Yükseklik, vinç, saha zorluğu."),
        ("Adet", "Filo / zincir / toplu işlerde birim değişir."),
        ("Teklif", "Keşif sonrası netleşir — WhatsApp / telefon."),
    ],
    "totem-secim-rehberi": [
        ("Konum", "Yol kenarı, tesis girişi, otopark."),
        ("Okuma mesafesi", "Hız ve görüş açısı yüksekliği belirler."),
        ("Işık", "Gece yaklaşım ihtiyacı."),
        ("Temel", "Statik ve saha koşulları."),
        ("Pylon", "Aynı aile; ayrı doorway yok."),
        ("Indoor display", "Display/POS sayfasına aittir."),
        ("Ticari sayfa", "/hizmetler/totem/."),
    ],
}


def build_article(slug: str, title: str, primary: str, pk: str) -> None:
    sections = ARTICLE_BODY[slug]
    a5 = ARTICLE_A5[slug]
    body = [block(h, p(para)) for h, para in sections]
    # Related industries via primary service
    inds = SERVICE_INDUSTRIES.get(primary, ["perakende", "plaza-ofis"])[:2]
    ind_labels = {
        "fabrika-osb": "Fabrika & OSB",
        "restoran-cafe": "Restoran & Cafe",
        "saglik": "Sağlık",
        "plaza-ofis": "Plaza & Ofis",
        "insaat-santiye": "İnşaat & Şantiye",
        "perakende": "Perakende",
    }
    # Related projects for primary
    projs = SERVICE_DEPTH.get(primary, {}).get("related_projects", ["liman-kahve", "dortnal"])
    other_bilgi = [
        (f"/bilgi/{s}/", t, "İlgili rehber.")
        for s, t, _, _ in ARTICLES
        if s != slug
    ][:3]
    faqs = a5["faqs"] + [
        ("İlgili hizmet nerede?", f"/hizmetler/{primary}/ sayfasında."),
        ("Daha fazla rehber?", "/bilgi/ hub’ında."),
    ]
    html = f"""{head(title, f"{title} — eğitici rehber. Malt Studio bilgi merkezi.", f"{SITE}/bilgi/{slug}/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Bilgi","/bilgi/"),(title,None))}
    <div class="eyebrow">Knowledge · PK: {pk}</div>
    <h1>{title}</h1>
    <p class="lede">Eğitici içerik. Money H1 taşımaz; {ALL_SERVICES.get(primary, primary)} hizmetine destek verir.</p>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Bu yazının rolü", p(
        f"Owner PK: “{pk}”. Ticari niyet /hizmetler/{primary}/ sayfasındadır.",
        "Karşılaştırma, avantaj/dezavantaj ve satın alma ipuçları burada; üretim ve teklif keşifte netleşir.",
    ))}
    {''.join(body)}
    {block("Avantajlar", ul(a5["advantages"]))}
    {block("Dezavantajlar / dikkat", ul(a5["disadvantages"]))}
    {block("Sık yapılan hatalar", ul(a5["mistakes"]))}
    {block("Satın alma ipuçları", ul(a5["buying"]))}
    {block("Bakım notları", ul(a5["maintenance"]))}
    {block("Pratik ek notlar", p(*ARTICLE_EXPAND[slug], ARTICLE_LONG[slug], ARTICLE_BRIDGE[slug]))}
    {eeat_block("rehber")}
  </div>
</section>
{related_rail(
    services=[
        (f"/hizmetler/{primary}/", ALL_SERVICES.get(primary, primary), "Ticari owner."),
        *([(f"/hizmet-bolge/tekirdag-{primary}/", f"Tekirdağ {ALL_SERVICES.get(primary, primary)}", "Geo-money owner.")] if primary in A0 else []),
    ],
    knowledge=other_bilgi,
    projects=projs,
    industries=[(f"/sektorler/{i}/", ind_labels.get(i, i), "Dikey bağlam.") for i in inds],
)}
<section class="section-band">
  <div class="wrap"><h2>SSS</h2><div class="faq">{faq_html(faqs)}</div></div>
</section>
{cta_band("Uygulama için yazın", f"{ALL_SERVICES.get(primary, primary)} hakkında bilgi")}
{footer()}
</body></html>
"""
    write(ROOT / "bilgi" / slug / "index.html", html)


def build_bilgi_hub() -> None:
    items = cards([(f"/bilgi/{s}/", t, f"PK: {pk}", "Rehber") for s, t, _, pk in ARTICLES])
    html = f"""{head("Bilgi Merkezi | Tabela ve Reklam Rehberleri", "Tabela çeşitleri, karşılaştırmalar ve uygulama rehberleri.", f"{SITE}/bilgi/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Bilgi",None))}
    <h1>Bilgi</h1>
    <p class="lede">Eğitici katman. Hizmet sayfalarını destekler; onların H1’ini çalmaz.</p>
  </div>
</section>
<section class="page-main"><div class="wrap">{block("Nasıl okumalı?", p("Önce ihtiyacınızı seçin, sonra ilgili hizmete geçin.","Fiyat eğitimi teklif yerine geçmez."))}{eeat_block("rehber hub")}</div></section>
<section class="section-band paper-band"><div class="wrap"><div class="card-grid">{items}</div></div></section>
{related_rail(
    services=[(f"/hizmetler/{s}/", n, "Hizmet owner.") for s, n in list(A0.items())[:6]],
    projects=["liman-kahve", "mera-otel", "dortnal"],
    industries=[(f"/sektorler/{s}/", n, "Dikey.") for s, n, _ in INDUSTRIES[:4]],
)}
{cta_band("Rehberden uygulamaya geçin", "Bilgi sonrası teklif")}
{footer()}
</body></html>
"""
    write(ROOT / "bilgi" / "index.html", html)


def merge_sitemap() -> None:
    urls = [
        f"{SITE}/",
        f"{SITE}/hizmetler/",
        f"{SITE}/bolgeler/tekirdag/",
        f"{SITE}/projeler/",
        f"{SITE}/sektorler/",
        f"{SITE}/bilgi/",
    ]
    for s in A0:
        urls += [f"{SITE}/hizmetler/{s}/", f"{SITE}/hizmet-bolge/tekirdag-{s}/"]
    for s in A2:
        urls.append(f"{SITE}/hizmetler/{s}/")
    for slug, *_ in PROJECTS:
        urls.append(f"{SITE}/projeler/{slug}/")
    for slug, *_ in INDUSTRIES:
        urls.append(f"{SITE}/sektorler/{slug}/")
    for slug, *_ in ARTICLES:
        urls.append(f"{SITE}/bilgi/{slug}/")
    body = "\n".join(
        f"""  <url>
    <loc>{u}</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if u.endswith("maltstudio.co/") else "0.7"}</priority>
  </url>"""
        for u in urls
    )
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n',
        encoding="utf-8",
    )
    print("sitemap", len(urls))


def main() -> None:
    build_hizmetler_hub()
    for slug in ALL_SERVICES:
        build_service(slug)
    for slug in A0:
        build_sxc(slug)
    build_city()
    build_projeler_hub()
    for slug, name, ind, svcs in PROJECTS:
        build_project(slug, name, ind, svcs)
    build_sektorler_hub()
    for slug, name, pk in INDUSTRIES:
        build_industry(slug, name, pk)
    build_bilgi_hub()
    for slug, title, primary, pk in ARTICLES:
        build_article(slug, title, primary, pk)
    merge_sitemap()
    # Wave A3 homepage authority (no new URLs)
    import importlib.util

    a3_path = ROOT / "scripts" / "build_home_a3.py"
    spec = importlib.util.spec_from_file_location("build_home_a3", a3_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    mod.main()
    print("Production upgrade complete. URL count frozen.")


if __name__ == "__main__":
    main()
