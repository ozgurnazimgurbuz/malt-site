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
    ADDRESS_COUNTRY,
    ADDRESS_LOCALITY,
    ADDRESS_ONE_LINE,
    ADDRESS_POSTAL,
    ADDRESS_REGION,
    ADDRESS_STREET,
    EMAIL,
    HOURS_DISPLAY,
    PHONE_DISPLAY,
    PHONE_TEL,
    ROOT,
    SITE,
    breadcrumb_ld,
    cards,
    crumbs,
    cta_band,
    eeat_block,
    faq_html,
    footer,
    head,
    header,
    mid_cta,
    page_graph,
    process_steps,
    related_rail,
    service_ld,
    wa,
    webpage_ld,
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


def tr_service_phrase(name: str) -> str:
    """Customer-facing phrase after 'Tekirdağ’da …' without broken Turkish lowercasing."""
    mapping = {
        "Tabela": "tabela üretimi ve montajı",
        "Işıklı Tabela": "ışıklı tabela hizmeti",
        "Kutu Harf": "kutu harf üretimi",
        "Totem": "totem tabela uygulamaları",
        "Araç Giydirme": "araç giydirme hizmeti",
        "Cam Giydirme": "cam giydirme uygulamaları",
        "Lightbox": "lightbox hizmeti",
        "Display & POS": "display ve POS uygulamaları",
        "Ofis Branding": "ofis branding uygulamaları",
        "İş Güvenliği Tabelaları": "iş güvenliği tabelaları",
    }
    return mapping.get(name, f"{name} hizmeti")


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
        "h1": "Tekirdağ Tabela İmalatı ve Montajı",
        "pk": "tabela",
        "title": "Tekirdağ Tabela İmalatı ve Montajı | Malt Studio",
        "desc": "Tekirdağ tabela üretimi: ışıklı ve ışıksız tabela, kutu harf, kompozit cephe ve mağaza tabelası. Keşif, imalat ve montaj için teklif alın.",
        "service_type": "Tabela üretimi ve montajı",
        "lede": "Ölçüye özel tabela üretimi: doğru malzeme, okunur tasarım ve güvenli montaj.",
        "extra": [
            "Tabela, markanın sokaktaki ve tesis girişindeki kalıcı imzasıdır. Doğru tabela; mesafeden okunur, malzemesi sahaya uygundur ve montajı uzun ömürlü planlanır.",
            "Işıksız kompozit tabeladan ışıklı sistemlere, iç yön tabelasından cephe kimliğine kadar ihtiyaçlar değişir.",
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
        "h1": "Tekirdağ Işıklı Tabela Üretim ve Montaj",
        "pk": "ışıklı tabela",
        "title": "Tekirdağ Işıklı Tabela | LED Üretim ve Montaj | Malt Studio",
        "desc": "Tekirdağ’da LED ışıklı tabela üretimi ve montajı. Gece görünür mağaza ve kurumsal tabelalar için keşif ve teklif.",
        "service_type": "Işıklı tabela üretimi ve montajı",
        "lede": "Gündüz taşıyan, gece de okunan LED ışıklı tabela sistemleri.",
        "extra": [
            "Işıklı tabela; kasa, LED modül, güç kaynağı ve yüzey malzemesinin birlikte çalıştığı bir üründür. Amaç gece saatlerinde de markayı okunur kılmaktır.",
            "Lightbox (ışıklı kutu / SEG) ayrı üründür ve /hizmetler/lightbox/ altındadır.",
            "Cephe derinliği, elektrik hattı ve servis erişimi keşifte kontrol edilir. Yanlış LED yoğunluğu hem ışığı bozar hem servisi zorlaştırır.",
            "Mağaza, eczane, klinik ve plaza girişlerinde gece trafiği varsa ışıklı sistem çoğu zaman doğru yatırımdır.",
            "Tekirdağ ve Süleymanpaşa keşifleri atölyeden planlanır.",
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
        "h1": "Tekirdağ Kutu Harf Tabela",
        "pk": "kutu harf",
        "title": "Tekirdağ Kutu Harf Tabela | Malt Studio",
        "desc": "Tekirdağ’da kutu harf tabela üretimi ve montajı. Pleksi, paslanmaz ve ışıklı kutu harf.",
        "service_type": "Kutu harf tabela üretimi ve montajı",
        "lede": "Cepheye derinlik katan ölçüye özel kutu harf sistemleri.",
        "extra": [
            "Kutu harf (channel letters), marka adını üç boyutlu taşıyan cephe yazısıdır. Pleksi ve paslanmaz en sık malzeme aileleridir.",
            "Channel letters ayrı bir ürün adı değildir; kutu harf ailesinde anlatılır.",
            "Harf yüksekliği, derinlik, ışıklı/ışıksız tercih ve montaj yüzeyi okunurluğu belirler.",
            "Plaza, ofis ve mağaza cephelerinde prestij algısını en hızlı yükselten uygulamalardan biridir.",
            "Tekirdağ plaza ve mağaza cephelerinde keşif sonrası ölçüye özel üretilir.",
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
        "h1": "Tekirdağ Totem Tabela",
        "pk": "totem tabela",
        "title": "Tekirdağ Totem Tabela | Üretim ve Montaj | Malt Studio",
        "desc": "Tekirdağ’da totem tabela üretimi ve montajı. Tesis girişi ve yol kenarı sistemleri.",
        "service_type": "Totem tabela üretimi ve montajı",
        "lede": "Uzaktan görülen, yönlendiren totem tabela sistemleri.",
        "extra": [
            "Totem; yol kenarı, tesis girişi ve otopark yaklaşımında markayı ve yönü taşır.",
            "Pylon/monument alt tipleri bu sayfada anlatılır; ayrı doorway URL açılmaz.",
            "Taşınabilir indoor display totem /hizmetler/display-pos/ ailesindedir.",
            "Yükseklik, temel, ışıklı tercih ve görüş mesafesi keşifte hesaplanır.",
            "Tekirdağ tesis ve OSB girişlerinde keşif sonrası temel ve yükseklik netleşir.",
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
        "h1": "Tekirdağ Araç Giydirme",
        "pk": "araç giydirme",
        "title": "Tekirdağ Araç Giydirme | Ticari Araç ve Filo | Malt Studio",
        "desc": "Tekirdağ’da ticari araç ve filo giydirme. Baskı, uygulama ve keşif için teklif alın.",
        "service_type": "Araç giydirme",
        "lede": "Filo ve ticari araçlarda tutarlı, dayanıklı giydirme uygulamaları.",
        "extra": [
            "Araç giydirme; baskılı folyonun araca uygulanmasıyla mobil marka yüzeyi oluşturur.",
            "Full wrap ve parça giydirme bu hizmetin alt uygulamalarıdır.",
            "Folyo baskı üretim adımıdır; sonuç ürün bu sayfada hedeflenir.",
            "Filo işlerinde şablon standardı ve araç tipi uyarlaması kritiktir.",
            "Tekirdağ merkezli filolar için uygulama atölyeden planlanır.",
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
        "h1": "Tekirdağ Cam Giydirme",
        "pk": "cam giydirme",
        "title": "Tekirdağ Cam Giydirme | One Way Vision ve Folyo | Malt Studio",
        "desc": "Tekirdağ’da cam giydirme: one way vision, vitrin ve cam folyo uygulamaları.",
        "service_type": "Cam giydirme",
        "lede": "Vitrin ve camda görünürlük, gizlilik ve mesaj dengesini kuran uygulamalar.",
        "extra": [
            "Cam giydirme; OWV, transparan/baskılı folyo ve vitrin grafiklerini kapsar.",
            "Window graphics / cam yazısı / vitrin reklamı aynı ailededir; ayrı URL yok.",
            "Ofis gizlilik paketi ofis branding ile birlikte yönetilebilir; malzeme bilgisi burada.",
            "Mağaza kampanyalarında hızlı yenileme avantajı sağlar.",
            "Tekirdağ mağaza vitrinlerinde keşif sonrası uygulanır.",
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
        "h1": "Tekirdağ Lightbox Tabela",
        "pk": "lightbox",
        "title": "Tekirdağ Lightbox Tabela | Işıklı Kutu ve Backlit | Malt Studio",
        "service_type": "Lightbox tabela üretimi ve montajı",
        "desc": "Lightbox, ışıklı kutu, SEG ve backlit frame sistemleri.",
        "lede": "İnce kasa lightbox ve ışıklı kutu sistemleriyle premium aydınlatmalı görsel alanlar.",
        "extra": [
            "Lightbox; arkadan veya kenardan aydınlatmalı çerçeve sistemidir. Retail ve AVM’de sık tercih edilir.",
            "Işıklı tabela / LED cephe sistemleri ayrı sayfadadır: /hizmetler/isikli-tabela/. Bu sayfa lightbox ailesidir.",
            "SEG / backlit fabric hızlı görsel değişimi sağlar.",
            "Yerel talep Tekirdağ üssünden keşif ile yönetilir.",
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
            "Tam fuar standı / backdrop ayrı değerlendirilir; tekil display burada planlanır.",
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
            ("Fuar standı?", "Tekil display burada planlanır; tam stand ayrıca değerlendirilir."),
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


def service_process(title: str = "Süreç"):
    return process_steps(
        [
            ("Keşif", "Ölçü, yüzey, erişim ve ihtiyaç netleştirilir."),
            ("Tasarım onayı", "Görsel ve teknik onay alınır."),
            ("Üretim", "Atölyede imalat ve kontrol."),
            ("Uygulama", "Saha montajı / giydirme."),
            ("Teslim", "Kontrol ve teslim notları."),
        ],
        title=title,
    )


def build_service(slug: str) -> None:
    s = SERVICE_DEPTH[slug]
    a5 = SERVICE_A5[slug]
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
        (f"/sektorler/{i}/", ind_labels.get(i, i), f"{ind_labels.get(i, i)} projeleri.")
        for i in SERVICE_INDUSTRIES.get(slug, [])
    ]
    services = [
        (f"/hizmetler/{r}/", ALL_SERVICES[r], f"{ALL_SERVICES[r]} hizmeti.")
        for r in s["related_services"]
        if r in ALL_SERVICES
    ]
    knowledge = [(b, "Rehber", "Karar vermenize yardımcı rehber.") for b in s["bilgi"]]
    local_h2 = (
        "Süleymanpaşa ve çevre ilçelerde tabela montajı"
        if slug == "tabela"
        else "Süleymanpaşa ve çevre ilçelerde montaj"
    )
    local_extra = block(
        local_h2,
        p(
            "Keşif ve montaj Tekirdağ Süleymanpaşa atölyesinden planlanır.",
            'Adres, saat ve iletişim: <a href="/bolgeler/tekirdag/">Malt Studio Tekirdağ atölye ve iletişim</a>.',
        ),
    )
    if slug == "tabela":
        intro = block(
            "Tekirdağ’da ürettiğimiz tabela çeşitleri",
            p(*s["extra"], *a5["intro"]) + ul(s["apps"]),
        )
        choice = block(
            "Işıklı, ışıksız, kutu harf veya kompozit: hangisi?",
            p(
                s["materials"],
                *a5["materials_extra"],
                'Gece görünürlük için <a href="/hizmetler/isikli-tabela/">ışıklı tabela seçenekleri</a>, cephe yazısı için <a href="/hizmetler/kutu-harf/">kutu harf tabela</a>, yol/tesis için <a href="/hizmetler/totem/">totem tabela üretimi</a>.',
            ),
        )
        proof = block(
            "Gerçek Tekirdağ tabela projeleri",
            p(
                'Seçili işler ana sayfada yer alır: <a href="/#isler">gerçek Tekirdağ tabela ve uygulama projeleri</a>.',
                'Liste: <a href="/projeler/">projeler</a>.',
            ),
        )
        price = block(
            "Tabela fiyatını belirleyen ölçü, malzeme ve montaj koşulları",
            p(
                "Ölçü, malzeme, ışıklı/özel üretim, montaj yüksekliği, saha lojistiği ve adet fiyatı belirler.",
                "Sabit internet fiyat listesi yayınlanmaz; keşif sonrası net teklif verilir.",
                'Ayrıntı: <a href="/bilgi/tabela-fiyati/">tabela fiyatını neler etkiler</a>.',
            ),
        )
        process = service_process("Keşiften montaja çalışma sürecimiz") + p(*a5["process_extra"])
        body_blocks = intro + choice + proof + price + process + eeat_block("hizmet") + local_extra
    else:
        body_blocks = (
            block("Bu hizmet nedir?", p(*s["extra"], *a5["intro"]))
            + block("Nerelerde kullanılır?", ul(s["apps"]) + p(*a5["where"]))
            + block("Malzeme ve seçenekler", p(s["materials"], *a5["materials_extra"]))
            + service_process()
            + block("Süreç notları", p(*a5["process_extra"]))
            + eeat_block("hizmet")
            + block("Deneyim ve üretim", p(*a5["eeat"]))
            + block(
                "Fiyatı neler etkiler?",
                p(
                    "Ölçü, malzeme, ışıklı/özel üretim, montaj yüksekliği, saha lojistiği ve adet fiyatı belirler.",
                    "Sabit internet fiyat listesi yayınlanmaz; keşif sonrası net teklif verilir.",
                ),
            )
            + block("Bakım ve sonrası", p(*a5["maintenance"]))
            + local_extra
        )
    json_ld = page_graph(
        webpage_ld(canonical, s["title"], s["desc"]),
        service_ld(canonical, s["h1"], s.get("service_type") or s["h1"]),
        breadcrumb_ld(
            [
                ("Ana Sayfa", "/"),
                ("Hizmetler", "/hizmetler/"),
                (s["h1"], canonical),
            ]
        ),
    )

    html = f"""{head(s["title"], s["desc"], canonical, json_ld=json_ld)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Hizmetler", "/hizmetler/"), (s["h1"], None))}
    <div class="eyebrow">Hizmet</div>
    <h1>{s["h1"]}</h1>
    <p class="lede">{s["lede"]}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa(f"Merhaba, {s['h1']} hakkında teklif almak istiyorum.")}" target="_blank" rel="noopener">Teklif Al</a>
      <a class="btn btn-ghost" href="{wa(f"Merhaba, {s['h1']} hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Telefon</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {body_blocks}
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
        "tabela": "Tekirdağ merkez ve Süleymanpaşa çarşı aksında mağaza tabela talepleri yoğundur. OSB koridoruna giden işler Tekirdağ üssünden planlanır. Çorlu ve Çerkezköy için de hizmet veriyoruz, iletişime geçebilirsiniz.",
        "isikli-tabela": "Tekirdağ’da gece açık kalan ticaret ve plaza cephelerinde LED ışıklı tabela sık istenir. Lightbox ihtiyacı ayrıca ayrılır.",
        "kutu-harf": "Tekirdağ plaza ve ofis cephelerinde kutu harf, prestij algısını hızlı yükseltir. Channel letters aynı ailede değerlendirilir.",
        "totem": "Tesis girişi ve yol yaklaşımında totem, Tekirdağ çevre sanayi taleplerinde öne çıkar. Temel/montaj keşifle planlanır.",
        "arac-giydirme": "Tekirdağ merkezli filolar ve ticari araçlar için giydirme, lojistik görünürlüğü artırır.",
        "cam-giydirme": "Tekirdağ mağaza vitrinlerinde OWV ve kampanya folyosu hızlı yenilenebilir yüzey sağlar.",
    }[slug]
    faqs = [
        (f"Tekirdağ’da {name.lower()} yaptırabilir miyim?", f"Evet, Tekirdağ’da {tr_service_phrase(name)} yapıyoruz."),
        ("Genel hizmet sayfasından farkı?", "Bu sayfa özellikle Tekirdağ’daki müşterilerimize yöneliktir."),
        ("Süleymanpaşa ayrı mı?", "Hayır; Süleymanpaşa talepleri Tekirdağ hizmet sayfalarında toplanır."),
        ("Fiyat?", "Yerel erişim + ölçü/malzeme/montaj keşifle netleşir."),
        ("Keşif?", "Tekirdağ üssünden planlanır."),
        ("Proje örneği?", "İlgili proje sayfalarına bakın; görseller eklendikçe güçlenir."),
    ]
    others = cards(
        [
            (f"/hizmet-bolge/tekirdag-{o}/", f"Tekirdağ {A0[o]}", f"Tekirdağ’da {tr_service_phrase(A0[o])}.", "Yerel")
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
    <div class="eyebrow">Tekirdağ’da Hizmet</div>
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
        "Bu sayfa Tekirdağ’daki yerel üretim, montaj ve lojistik bağlamını taşır.",
        "Süleymanpaşa ve merkez talepleri bu sayfada toplanır.",
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
        (f"/hizmetler/{slug}/", name, f"{name} genel hizmet sayfası."),
        *[(f"/hizmetler/{r}/", ALL_SERVICES[r], f"{ALL_SERVICES[r]} hizmeti.") for r in s["related_services"] if r in ALL_SERVICES][:3],
    ],
    knowledge=[(b, "Rehber", "Eğitim.") for b in s["bilgi"]],
    projects=s["related_projects"],
    industries=[
        (f"/sektorler/{i}/", {"fabrika-osb":"Fabrika & OSB","restoran-cafe":"Restoran & Cafe","saglik":"Sağlık","plaza-ofis":"Plaza & Ofis","insaat-santiye":"İnşaat & Şantiye","perakende":"Perakende"}.get(i,i), "Sektöre özel çözümler.")
        for i in SERVICE_INDUSTRIES.get(slug, [])[:2]
    ],
    hubs=[
        ("/bolgeler/tekirdag/", "Tekirdağ", "Tekirdağ yerel hizmet rehberi."),
        ("/hizmetler/", "Hizmetler", "Tüm hizmetlerimize göz atın."),
        ("/projeler/", "Projeler", "Tamamladığımız işlerden örnekler."),
        ("/", "Ana sayfa", "Malt Studio ana sayfa."),
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
    title = "Malt Studio Tekirdağ Atölye ve İletişim"
    desc = "Malt Studio’nun Tekirdağ Süleymanpaşa iletişim, çalışma saatleri, hizmet alanları ve keşif bilgileri. Telefon, WhatsApp ve yol tarifi."
    svc = cards([(f"/hizmetler/{s}/", n, f"{n} hizmeti.", "Hizmet") for s, n in A0.items()])
    faqs = [
        ("Atölye nerede?", f"{ADDRESS_ONE_LINE}."),
        ("Çalışma saatleri?", HOURS_DISPLAY + "."),
        ("Süleymanpaşa ayrı sayfa mı?", "Hayır; Süleymanpaşa talepleri bu atölye sayfasında toplanır."),
        ("Keşif nasıl alınır?", "WhatsApp veya telefon ile kısa brief bırakın."),
    ]
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        breadcrumb_ld([("Ana Sayfa", "/"), (title, canonical)]),
    )
    html = f"""{head(title, desc, canonical, json_ld=json_ld)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Tekirdağ",None))}
    <div class="eyebrow">Atölye</div>
    <h1>{title}</h1>
    <p class="lede">Adres, telefon, e-posta ve keşif bilgisi. Bu sayfa ikinci bir reklam ajansı landing’i değildir.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa("Tekirdağ keşif")}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara</a>
      <a class="btn btn-ghost" href="/hizmetler/">Hizmetler</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("İletişim", p(
        f"<strong>Adres:</strong> {ADDRESS_STREET}<br>{ADDRESS_POSTAL} {ADDRESS_LOCALITY} / {ADDRESS_REGION}<br>{ADDRESS_COUNTRY}",
        f'<strong>Telefon:</strong> <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>',
        f'<strong>E-posta:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a>',
        f"<strong>Çalışma saatleri:</strong> {HOURS_DISPLAY}",
        'WhatsApp veya telefon ile keşif randevusu alınır.',
    ))}
    {block("Ulaşım", p(
        "Atölye Süleymanpaşa / Tekirdağ’dadır. Keşif randevusu sonrası ölçü ve montaj planı çıkarılır.",
        "Yol tarifi için Google Haritalar’da Malt Studio veya adresi arayın.",
    ))}
    {block("Hizmet bölgeleri", p(
        "Süleymanpaşa ve Tekirdağ merkez başta olmak üzere çevre ilçelere keşif ve montaj planlanır.",
        "Çorlu, Çerkezköy, Kapaklı, Ergene, Muratlı ve diğer ilçe işleri aynı atölyeden yönetilir.",
    ))}
    {block("Gerçek işler", p(
        'Ana sayfadaki <a href="/#isler">seçili işler</a> gerçek saha fotoğraflarıdır.',
        'Hizmet sayfaları: <a href="/hizmetler/tabela/">tabela</a>, <a href="/hizmetler/isikli-tabela/">ışıklı tabela</a>, <a href="/hizmetler/kutu-harf/">kutu harf</a>.',
    ))}
    {mid_cta("Tekirdağ keşif")}
  </div>
</section>
{related_rail(
    services=[(f"/hizmetler/{s}/", n, f"{n} hizmeti.") for s, n in list(A0.items())[:6]],
    knowledge=[(f"/bilgi/{s}/", t, "Rehber.") for s, t, _, _ in ARTICLES[:4]],
    industries=[(f"/sektorler/{s}/", n, f"{n} çözümleri.") for s, n, _ in INDUSTRIES[:4]],
)}
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Hizmetler</h2>
    <div class="card-grid">{svc}</div>
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
    a0 = cards([(f"/hizmetler/{s}/", n, f"{n} hizmeti.", "Hizmet") for s, n in A0.items()])
    a2 = cards([(f"/hizmetler/{s}/", n, f"{n} hizmeti.", "Hizmet") for s, n in A2.items()])
    html = f"""{head("Hizmetler | Tabela, Lightbox, Ofis Branding ve Daha Fazlası", "Malt Studio tüm hizmetleri: tabela, ışıklı tabela, kutu harf, totem, araç ve cam giydirme, lightbox, display, ofis branding, İSG.", f"{SITE}/hizmetler/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Hizmetler",None))}
    <div class="eyebrow">Hizmetler</div>
    <h1>Hizmetler</h1>
    <p class="lede">Tabela üretiminden montaja, ihtiyacınıza uygun hizmetler.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa("Hizmet seçimi için yardımcı olur musunuz?")}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Nasıl seçmelisiniz?", p(
        "Önce ihtiyacı netleştirin: cephe tabela, ışıklı sistem, kutu harf, araç, cam, lightbox, display veya ofis paketi.",
        'Kararsızsanız <a href="/bilgi/">rehberleri</a> okuyun veya WhatsApp ile kısa keşif isteyin.',
        "Tekirdağ atölye ve iletişim için /bolgeler/tekirdag/ sayfasına bakın.",
    ))}
    {eeat_block("hizmet hub")}
    {mid_cta("Hizmet seçimi için yardımcı olur musunuz?")}
  </div>
</section>
{related_rail(
    knowledge=[(f"/bilgi/{s}/", t, "Rehber.") for s, t, _, _ in ARTICLES[:4]],
    industries=[(f"/sektorler/{s}/", n, f"{n} çözümleri.") for s, n, _ in INDUSTRIES[:4]],
)}
<section class="section-band paper-band">
  <div class="wrap"><h2>Çekirdek hizmetler</h2><div class="card-grid">{a0}</div></div>
</section>
<section class="section-band">
  <div class="wrap"><h2>Ek hizmetler</h2><div class="card-grid">{a2}</div></div>
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
        [(href, label, "Karar vermenize yardımcı rehber.", "Bilgi") for href, label in _knowledge_for(services)]
    )
    rel = case["related_projects"]
    rel_cards = cards(
        [
            (
                f"/projeler/{s}/",
                CASES[s]["name"] if s in CASES else s,
                "Benzer proje örneği.",
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
</dl>"""

    applied = "<ul class='scope-list'>" + "".join(
        f"<li><a href='/hizmetler/{s}/'>{ALL_SERVICES[s]}</a></li>"
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
    <div class="eyebrow">Proje</div>
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
    {block("Uygulanan hizmetler", applied)}
    {block("Üretim süreci", p(*case["process"]))}
    {block("Montaj / uygulama", p(*case["installation"]))}
    {block("Kullanılan malzemeler", p(*case["materials"]))}
    {block("Teknik detaylar", p(*case["technical"]))}
    {block("Sonuç", p(*case["result"]))}
    <div class="content-block">
      <h2>Proje Görselleri</h2>
      <p class="awaiting">Bu projenin saha ve teslim fotoğrafları yakında eklenecek.</p>
      <ul>
        <li>Atölye üretimi ve saha montajı aynı operasyonel hat üzerinden planlanır.</li>
        <li>Yayın öncesi müşteri onayı alınır.</li>
      </ul>
    </div>
  </div>
</section>
{evidence_gallery(name)}
<section class="section-band paper-band" aria-labelledby="applied-services-title">
  <div class="wrap">
    <h2 id="applied-services-title">İlgili hizmetler</h2>
    <p class="intro">Bu projede kullandığımız hizmetler.</p>
    <div class="card-grid">{svc_cards}</div>
  </div>
</section>
<section class="section-band" aria-labelledby="related-industry-title">
  <div class="wrap">
    <h2 id="related-industry-title">İlgili sektör</h2>
    <div class="card-grid">{cards([
        (f"/sektorler/{industry}/", ind_label, "Dikey bağlam sayfası.", "Sektör"),
        ("/bolgeler/tekirdag/", "Tekirdağ", "Tekirdağ yerel hizmet rehberi.", "City"),
        ("/projeler/", "Tüm projeler", "Tüm proje örnekleri.", "Proje"),
    ])}</div>
  </div>
</section>
<section class="section-band paper-band" aria-labelledby="related-knowledge-title">
  <div class="wrap">
    <h2 id="related-knowledge-title">İlgili rehberler</h2>
    <p class="intro">Karar vermenize yardımcı olacak rehberler.</p>
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
    ("/projeler/", "Projeler", "Tamamladığımız işlerden örnekler."),
    ("/hizmetler/", "Hizmetler", "Tüm hizmetlerimize göz atın."),
    ("/bilgi/", "Bilgi", "Rehberler ve karar içerikleri."),
    ("/sektorler/", "Sektörler", "Sektöre özel çözümler."),
    ("/bolgeler/tekirdag/", "Tekirdağ", "Tekirdağ yerel hizmet rehberi."),
    ("/", "Ana sayfa", "Malt Studio ana sayfa."),
])}
{project_cta(name)}
</article>
{footer()}
</body></html>
"""
    write(ROOT / "projeler" / slug / "index.html", html)


def build_projeler_hub() -> None:
    html = f"""{head("Projeler | Malt Studio İş Örnekleri", "Tabela, ışıklı tabela, kutu harf ve giydirme proje örnekleri.", f"{SITE}/projeler/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Projeler",None))}
    <h1>Projeler</h1>
    <p class="lede">Tamamladığımız işlerden örnekler. Görseller geldikçe güncellenir.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa("Yeni proje")}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Neden proje sayfaları?", p(
        "Gerçek saha fotoğrafları ana sayfada yer alır.",
        "Ayrı proje URL’si yalnızca içerik hazır olduğunda açılır.",
    ))}
    {eeat_block("proje hub")}
    {mid_cta("Yeni proje")}
  </div>
</section>
{related_rail(
    services=[(f"/hizmetler/{s}/", n, f"{n} hizmeti.") for s, n in list(A0.items())[:6]],
    knowledge=[(f"/bilgi/{s}/", t, "Rehber.") for s, t, _, _ in ARTICLES[:3]],
    industries=[(f"/sektorler/{s}/", n, f"{n} çözümleri.") for s, n, _ in INDUSTRIES[:4]],
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
        (f"/hizmetler/{s}/", ALL_SERVICES[s], f"{ALL_SERVICES[s]} hizmeti.")
        for s in services
        if s in ALL_SERVICES
    ]
    bil_links = [(h, "Rehber", "Karar vermenize yardımcı rehber.") for h in a5["knowledge"]]
    html = f"""{head(f"{name} Tabela ve Görünürlük Çözümleri", f"{name} sektörü için tabela ve görünürlük. Malt Studio.", f"{SITE}/sektorler/{slug}/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Sektörler","/sektorler/"),(name,None))}
    <div class="eyebrow">Sektör</div>
    <h1>{name}</h1>
    <p class="lede">{lede}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa(f"{name} sektörü keşif")}" target="_blank" rel="noopener">Teklif Al</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Telefon</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Sektör ihtiyacı", p(
        lede,
        "Bu sayfa sektör bağlamı sunar; teklif ilgili hizmet sayfalarından alınır.",
        "Tekirdağ üssünden keşif yapılır; koridor ilçeleri operasyonel kapsamda değerlendirilir.",
    ))}
    {block("Sık karşılaşılan sorunlar", ul(a5["problems"]))}
    {block("Tipik ihtiyaçlar", ul(needs))}
    {block("Önerilen hizmet seti", p(
        "Aşağıdaki hizmetler bu sektörde sık bir araya gelir.",
    ) + ul([ALL_SERVICES[s] for s in services if s in ALL_SERVICES]))}
    {block("Proje iş akışı", p(*a5["workflow"]))}
    {block("Malzeme önerileri", p(*a5["materials"]))}
    {block("Bakım ve saha notları", p(*a5["maintenance"]))}
    {block("Saha pratikleri", p(*INDUSTRY_EXPAND[slug], INDUSTRY_LONG[slug], INDUSTRY_BRIDGE[slug]))}
    {eeat_block("sektör")}
    {mid_cta(f"{name} sektörü keşif")}
  </div>
</section>
{related_rail(services=svc_links, knowledge=bil_links)}
<section class="section-band paper-band">
  <div class="wrap"><h2>SSS</h2><div class="faq">{faq_html([
      (f"{name} için hangi hizmetler?", ", ".join(ALL_SERVICES[s] for s in services if s in ALL_SERVICES)+"."),
      ("Bu hizmet sayfasının yerine geçer mi?", "Hayır; dikey girişidir."),
      ("Tekirdağ’da uygulanır mı?", "Evet; keşif Tekirdağ üssünden planlanır."),
      ("Teklif?", "WhatsApp veya telefon ile keşif talebi bırakın."),
  ])}</div></div>
</section>
{cta_band(f"{name} için keşif", f"{name} keşif")}
{footer()}
</body></html>
"""
    write(ROOT / "sektorler" / slug / "index.html", html)


def build_sektorler_hub() -> None:
    items = cards([(f"/sektorler/{s}/", n, f"{n} çözümleri.", "Sektör") for s, n, pk in INDUSTRIES])
    html = f"""{head("Sektörler | Fabrika, Restoran, Sağlık, Plaza", "Sektörel tabela ve görünürlük çözümleri.", f"{SITE}/sektorler/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Sektörler",None))}
    <h1>Sektörler</h1>
    <p class="lede">Farklı sektörlere özel görünürlük çözümleri.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa("Sektör keşfi")}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
    </div>
  </div>
</section>
<section class="page-main"><div class="wrap">{block("Nasıl kullanılır?", p("Sektörünüzü seçin, ilgili hizmetlere ve projelere geçin.","Kararsızsanız Tekirdağ hub veya WhatsApp ile yazın."))}{eeat_block("sektör hub")}{mid_cta("Sektör keşfi")}</div></section>
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
        ("Ticari sayfa", "/hizmetler/arac-giydirme/ ve Tekirdağ araç giydirme sayfası."),
    ],
    "tabela-fiyati": [
        ("Uyarı", "Bu sayfa fiyat eğitimidir; sabit fiyat listesi değildir. Net teklif keşif sonrası verilir."),
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
    svc_name = ALL_SERVICES.get(primary, primary)
    role_link = (
        f'Üretim ve teklif için <a href="/hizmetler/{primary}/">{svc_name}</a> '
        "sayfasına bakabilirsiniz."
    )
    wa_msg = f"{svc_name} hakkında bilgi"
    html = f"""{head(title, f"{title} — eğitici rehber. Malt Studio bilgi merkezi.", f"{SITE}/bilgi/{slug}/")}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Bilgi","/bilgi/"),(title,None))}
    <div class="eyebrow">Rehber</div>
    <h1>{title}</h1>
    <p class="lede">Eğitici rehber. {svc_name} hakkında karar vermenize yardımcı olur.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa(wa_msg)}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
      <a class="btn btn-ghost" href="/hizmetler/{primary}/">{svc_name} hizmeti</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Bu yazının rolü", p(
        role_link,
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
    {mid_cta(wa_msg)}
  </div>
</section>
{related_rail(
    services=[
        (f"/hizmetler/{primary}/", ALL_SERVICES.get(primary, primary), f"{ALL_SERVICES.get(primary, primary)} hizmeti."),
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
    <p class="lede">Tabela, malzeme ve süreç hakkında kısa rehberler.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa("Bilgi sonrası teklif")}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
    </div>
  </div>
</section>
<section class="page-main"><div class="wrap">{block("Nasıl okumalı?", p("Önce ihtiyacınızı seçin, sonra ilgili hizmete geçin.","Fiyat eğitimi teklif yerine geçmez."))}{eeat_block("rehber hub")}{mid_cta("Bilgi sonrası teklif")}</div></section>
<section class="section-band paper-band"><div class="wrap"><div class="card-grid">{items}</div></div></section>
{related_rail(
    services=[(f"/hizmetler/{s}/", n, f"{n} hizmeti.") for s, n in list(A0.items())[:6]],
    projects=["liman-kahve", "mera-otel", "dortnal"],
    industries=[(f"/sektorler/{s}/", n, f"{n} çözümleri.") for s, n, _ in INDUSTRIES[:4]],
)}
{cta_band("Rehberden uygulamaya geçin", "Bilgi sonrası teklif")}
{footer()}
</body></html>
"""
    write(ROOT / "bilgi" / "index.html", html)


def merge_sitemap() -> None:
    """Indexable owner URLs only. lastmod only on pages rewritten this pass."""
    updated = {
        f"{SITE}/",
        f"{SITE}/hizmetler/",
        f"{SITE}/bolgeler/tekirdag/",
        f"{SITE}/projeler/",
    }
    for s in ALL_SERVICES:
        updated.add(f"{SITE}/hizmetler/{s}/")
    urls = [
        f"{SITE}/",
        f"{SITE}/hizmetler/",
        f"{SITE}/bolgeler/tekirdag/",
        f"{SITE}/projeler/",
        f"{SITE}/sektorler/",
        f"{SITE}/bilgi/",
    ]
    for s in ALL_SERVICES:
        urls.append(f"{SITE}/hizmetler/{s}/")
    for slug, *_ in INDUSTRIES:
        urls.append(f"{SITE}/sektorler/{slug}/")
    for slug, *_ in ARTICLES:
        urls.append(f"{SITE}/bilgi/{slug}/")
    parts = []
    for u in urls:
        if u in updated:
            parts.append(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>2026-08-11</lastmod>\n  </url>")
        else:
            parts.append(f"  <url>\n    <loc>{u}</loc>\n  </url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(parts)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    print("sitemap", len(urls))


def main() -> None:
    build_hizmetler_hub()
    for slug in ALL_SERVICES:
        build_service(slug)
    build_city()
    build_projeler_hub()
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
