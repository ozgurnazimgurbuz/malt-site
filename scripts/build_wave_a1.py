#!/usr/bin/env python3
"""Wave A1: Projects, Industries, Knowledge only. Does not modify A0 page files."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://maltstudio.co"
PHONE_DISPLAY = "0552 582 69 59"
PHONE_TEL = "+905525826959"
WA = "905525826959"
EMAIL = "merhaba@maltstudio.com"

# A0 service map (link targets only — do not rewrite those pages)
SERVICES = {
    "tabela": "Tabela",
    "isikli-tabela": "Işıklı Tabela",
    "kutu-harf": "Kutu Harf",
    "totem": "Totem",
    "arac-giydirme": "Araç Giydirme",
    "cam-giydirme": "Cam Giydirme",
}

PROJECTS = [
    {
        "slug": "liman-kahve",
        "name": "Liman Kahve",
        "industry": "restoran-cafe",
        "city": "Tekirdağ",
        "city_href": "/bolgeler/tekirdag/",
        "services": ["tabela", "isikli-tabela", "cam-giydirme"],
        "problem": "Mağaza cephesi ve vitrin, markayı uzaktan ve gece saatlerinde yeterince taşımıyordu.",
        "objectives": [
            "Cephede net isim okunurluğu",
            "Gece görünür ışıklı yüzey",
            "Vitrinde kampanya / menü mesaj alanı",
        ],
        "production": "Işıklı tabela kasası ve vitrin folyo ölçüleri atölyede üretildi; uygulama saha montajıyla tamamlandı.",
        "materials": "LED ışıklı kasa, kompozit yan paneller, one way / vitrin folyo.",
        "installation": "Cephe montajı ve cam uygulama aynı programda planlandı.",
        "challenges": "Dar kaldırım ve çalışma saati kısıtı nedeniyle montaj penceresi kısa tutuldu.",
        "results": "Marka gece-gündüz okunur hale geldi; vitrin mesaj alanı yenilenebilir bırakıldı.",
        "note": "Görseller ve ölçü detayları müşteri onayı sonrası eklenecektir. EEAT için gerçek foto şarttır.",
    },
    {
        "slug": "volt-enerji",
        "name": "Volt Enerji",
        "industry": "fabrika-osb",
        "city": "Tekirdağ",
        "city_href": "/bolgeler/tekirdag/",
        "services": ["totem", "tabela", "kutu-harf"],
        "problem": "Tesis yaklaşımında kurumsal kimlik ve yön bulma zayıftı.",
        "objectives": [
            "Girişte güçlü tesis kimliği",
            "Yönlendirme ve okunabilirlik",
            "Dayanıklı dış mekan malzeme",
        ],
        "production": "Totem konstrüksiyonu ve cephe yazı elemanları atölyede imal edildi.",
        "materials": "Çelik/alüminyum konstrüksiyon, kompozit yüzey, kutu harf.",
        "installation": "Saha montajı ve hizalama keşif ölçülerine göre yapıldı.",
        "challenges": "Açık saha rüzgâr yükü ve temel/montaj koordinasyonu.",
        "results": "Tesis girişi uzaktan tanımlanabilir hale geldi.",
        "note": "Sanayi projelerinde saha fotoğrafları yayın öncesi onay ister.",
    },
    {
        "slug": "kuzey-tekstil",
        "name": "Kuzey Tekstil",
        "industry": "fabrika-osb",
        "city": "Tekirdağ",
        "city_href": "/bolgeler/tekirdag/",
        "services": ["tabela", "arac-giydirme", "totem"],
        "problem": "Üretim tesisi ve filo araçlarında tutarsız marka dili vardı.",
        "objectives": [
            "Tesis tabela standardı",
            "Filoda tutarlı giydirme",
            "Lojistik görünürlük",
        ],
        "production": "Tabela ve araç folyo baskıları aynı marka dosyasından üretildi.",
        "materials": "Kompozit tabela, araç folyo, laminasyon (ihtiyaca göre).",
        "installation": "Tesis montajı ve araç uygulaması ayrı günlerde tamamlandı.",
        "challenges": "Filo araçlarının farklı ölçülerine şablon uyarlama.",
        "results": "Tesis + filo tek görsel dilde birleşti.",
        "note": "Before/after görselleri eklenecek.",
    },
    {
        "slug": "mera-otel",
        "name": "Mera Otel",
        "industry": "plaza-ofis",
        "city": "Tekirdağ",
        "city_href": "/bolgeler/tekirdag/",
        "services": ["kutu-harf", "tabela", "isikli-tabela"],
        "problem": "Giriş ve cephe kimliği konaklama prestijiyle uyumsuzdu.",
        "objectives": [
            "Prestijli cephe yazısı",
            "Gece okunurluk",
            "Mimariyle uyum",
        ],
        "production": "Kutu harf ve ışıklı elemanlar ölçüye özel üretildi.",
        "materials": "Pleksi/paslanmaz kutu harf, LED, kompozit tamamlayıcılar.",
        "installation": "Cephe montajı misafir sirkülasyonu gözetilerek planlandı.",
        "challenges": "Yüksekte çalışma ve yüzey hazırlığı.",
        "results": "Giriş kimliği güçlendi; gece görünürlük arttı.",
        "note": "Otel/konaklama dikeyinde ek case’ler sektör sayfasında toplanır.",
    },
    {
        "slug": "dortnal",
        "name": "Dörtnal",
        "industry": "perakende",
        "city": "Tekirdağ",
        "city_href": "/bolgeler/tekirdag/",
        "services": ["isikli-tabela", "cam-giydirme", "tabela"],
        "problem": "Mağaza vitrin ve tabela seti kampanya değişimine uygun değildi.",
        "objectives": [
            "Işıklı mağaza kimliği",
            "Yenilenebilir vitrin yüzeyi",
            "Sokaktan hızlı algı",
        ],
        "production": "Işıklı tabela + cam giydirme birlikte üretildi.",
        "materials": "LED kasa, one way vision / vitrin folyo.",
        "installation": "Mağaza çalışma saatlerine göre kısa montaj penceresi.",
        "challenges": "Cam ölçü hassasiyeti ve kırılgan yüzey.",
        "results": "Mağaza cephesi güncellenebilir bir sisteme kavuştu.",
        "note": "Perakende paketleri sektör sayfasında anlatılır.",
    },
    {
        "slug": "ekip-yazilim",
        "name": "Ekip Yazılım",
        "industry": "plaza-ofis",
        "city": "Tekirdağ",
        "city_href": "/bolgeler/tekirdag/",
        "services": ["kutu-harf", "cam-giydirme", "tabela"],
        "problem": "Ofis girişi ve cam yüzeylerde kurumsal kimlik eksikti.",
        "objectives": [
            "Resepsiyon / giriş yazısı",
            "Cam grafik ile marka dili",
            "Sade kurumsal görünüm",
        ],
        "production": "Kutu harf ve cam folyo uygulamaları ofis ölçülerine göre hazırlandı.",
        "materials": "Kutu harf, kumlama/baskılı cam folyo, iç tabela.",
        "installation": "Mesai dışı uygulama ile ofis kesintisi azaltıldı.",
        "challenges": "Cam film hizası ve aydınlatma yansımaları.",
        "results": "Ofis girişi markayı karşılayan bir yüzey haline geldi.",
        "note": "Ofis branding genişlemesi sonraki hizmet dalgasında derinleşir.",
    },
]

INDUSTRIES = [
    {
        "slug": "fabrika-osb",
        "name": "Fabrika & OSB",
        "pk": "fabrika tabela",
        "title": "Fabrika ve OSB Tabela Çözümleri",
        "description": "Fabrika tabela, OSB tabela, tesis yönlendirme ve sanayi görünürlük çözümleri. Malt Studio.",
        "lede": "Sanayi tesislerinde okunur kimlik, yönlendirme ve dayanıklı dış mekan sistemleri.",
        "intro": "Fabrika ve OSB ortamında tabela; marka kadar güvenlik, lojistik ve ziyaretçi yönlendirmesidir. Bu sayfa dikey giriştir — tek hizmetin birincil anahtar kelimesini çalmaz.",
        "needs": [
            "Tesis giriş totemi ve cephe yazısı",
            "İç yönlendirme ve saha levhaları",
            "Filo araç giydirme",
            "Dayanıklı dış mekan malzemeler",
        ],
        "services": ["totem", "tabela", "kutu-harf", "arac-giydirme"],
        "district_bias": "Tekirdağ üssü; Çorlu / Çerkezköy koridoru sonraki şehir sayfalarında genişler.",
    },
    {
        "slug": "restoran-cafe",
        "name": "Restoran & Cafe",
        "pk": "restoran tabela",
        "title": "Restoran ve Cafe Tabela & Vitrin Çözümleri",
        "description": "Restoran tabela, cafe ışıklı tabela, vitrin giydirme ve menü görünürlüğü. Malt Studio.",
        "lede": "Sokaktan menüye kadar okunan bir restoran / cafe kimliği.",
        "intro": "F&B işletmelerinde tabela ve vitrin, ilk karar anını yönetir. Bu sayfa sektör paketidir; ışıklı tabela veya cam giydirme hizmet sayfalarının yerine geçmez.",
        "needs": [
            "Işıklı / ışıksız cephe tabela",
            "Vitrin ve cam giydirme",
            "Gece görünürlük",
            "Hızlı yenilenen kampanya yüzeyleri",
        ],
        "services": ["isikli-tabela", "cam-giydirme", "tabela", "kutu-harf"],
        "district_bias": "Tekirdağ merkez ve sahil talepleri City / S×C sayfalarıyla bağlanır.",
    },
    {
        "slug": "saglik",
        "name": "Sağlık",
        "pk": "klinik tabela",
        "title": "Klinik ve Sağlık Kurumu Tabela Çözümleri",
        "description": "Klinik tabela, poliklinik yönlendirme ve sağlık kurumları görünürlük sistemleri. Malt Studio.",
        "lede": "Sağlık noktalarında sakin, okunur ve güven veren görünürlük.",
        "intro": "Klinik ve polikliniklerde tabela; güven ve yön bulma demektir. Wayfinding derinliği sonraki yönlendirme hizmet sayfasıyla genişleyecektir.",
        "needs": [
            "Işıklı kurumsal tabela",
            "İç mekan yön tabela setleri",
            "Cam grafik / gizlilik dengesi",
            "Sade kurumsal dil",
        ],
        "services": ["isikli-tabela", "tabela", "kutu-harf", "cam-giydirme"],
        "district_bias": "Tekirdağ ve çevre ilçe sağlık noktaları.",
    },
    {
        "slug": "plaza-ofis",
        "name": "Plaza & Ofis",
        "pk": "ofis tabela",
        "title": "Plaza ve Ofis Tabela / Giriş Kimliği",
        "description": "Plaza tabela, ofis giriş yazısı, kutu harf ve cam grafik çözümleri. Malt Studio.",
        "lede": "Plaza ve ofis girişlerinde kurumsal ilk izlenim.",
        "intro": "Plaza / ofis dikeyi; kutu harf, tabela ve cam grafik paketlerini bir araya getirir. Ayrı ofis-branding hizmet URL’si sonraki dalgadadır — bu sayfa sektör girişidir.",
        "needs": [
            "Cephe kutu harf",
            "Giriş / kat tabela",
            "Cam folyo ve marka grafiği",
            "Işıklı logo uygulamaları",
        ],
        "services": ["kutu-harf", "tabela", "isikli-tabela", "cam-giydirme"],
        "district_bias": "Tekirdağ ve Çorlu plaza ekonomisi.",
    },
    {
        "slug": "insaat-santiye",
        "name": "İnşaat & Şantiye",
        "pk": "şantiye brandası",
        "title": "Şantiye Brandası ve Proje Tanıtım Panoları",
        "description": "Şantiye brandası, mesh, proje tanıtım panosu ve inşaat saha tabelaları. Malt Studio.",
        "lede": "Şantiye çevresinde proje mesajı ve saha görünürlüğü.",
        "intro": "İnşaat dikeyi ağırlıklı olarak geniş format baskı ve saha tabelasına dayanır. Germe/branda ayrı hizmet URL’si sonraki dalgada derinleşir; Wave A1’de dijital baskı ihtiyacı tabela + iletişim yoluyla karşılanır.",
        "needs": [
            "Proje tanıtım panoları",
            "Şantiye çevre mesajları",
            "Geçici yön ve uyarı yüzeyleri",
            "Hızlı üretim / saha montajı",
        ],
        "services": ["tabela", "totem", "cam-giydirme"],
        "district_bias": "Büyüme koridoru şantiyeleri — Tekirdağ üssünden lojistik.",
    },
    {
        "slug": "perakende",
        "name": "Perakende",
        "pk": "mağaza tabelası",
        "title": "Mağaza Tabela ve Vitrin Çözümleri",
        "description": "Mağaza tabelası, ışıklı tabela, vitrin giydirme ve perakende cephe paketleri. Malt Studio.",
        "lede": "Mağaza cephesini satışa açan tabela ve vitrin sistemleri.",
        "intro": "Perakende dikeyi storefront paketidir. ‘Mağaza tabelası’ niyeti burada karşılanır; ürün detayı ilgili hizmet sayfalarındadır.",
        "needs": [
            "Işıklı mağaza tabela",
            "Vitrin / one way vision",
            "Kampanya yenileme",
            "Açılış paketleri",
        ],
        "services": ["isikli-tabela", "cam-giydirme", "tabela", "kutu-harf"],
        "district_bias": "Tekirdağ çarşı ve cadde mağazaları.",
    },
]

ARTICLES = [
    {
        "slug": "tabela-cesitleri",
        "title": "Tabela Çeşitleri: Hangisi Ne İşe Yarar?",
        "description": "Tabela çeşitleri rehberi: ışıksız, ışıklı, kutu harf, totem ve cam uygulamaları. Malt Studio bilgi merkezi.",
        "pk": "tabela çeşitleri",
        "primary_service": "tabela",
        "intro": "Tabela seçimi sadece estetik değil; okunurluk, dayanım ve montaj koşullarının toplamıdır. Bu rehber bilgilendirme amaçlıdır — satın alma niyeti hizmet sayfalarına yönlenir.",
        "sections": [
            ("Işıksız tabela", "Gündüz odaklı, genelde daha ekonomik cephe çözümleri."),
            ("Işıklı tabela", "Gece görünürlük gereken mağaza ve hizmet noktaları için."),
            ("Kutu harf", "Cephede üç boyutlu marka yazısı; prestij ve derinlik."),
            ("Totem", "Yol / tesis yaklaşımında uzaktan algı."),
            ("Cam giydirme", "Vitrin mesajı ve gizlilik / görünürlük dengesi."),
        ],
        "mistakes": [
            "Sadece fiyata bakıp malzeme ömrünü yok saymak",
            "Montaj yüzeyini keşifsiz varsaymak",
            "Gece ihtiyacı varken ışıksız seçmek",
        ],
        "faqs": [
            ("En doğru tabela hangisi?", "Konum, bütçe ve gece ihtiyacına göre değişir; keşif gerekir."),
            ("Bu sayfadan sipariş verilir mi?", "Hayır. Bu bilgilendirme sayfasıdır; teklif için hizmet / WhatsApp kullanılır."),
        ],
    },
    {
        "slug": "isikli-mi-isiksiz-mi",
        "title": "Işıklı Tabela mı Işıksız mı?",
        "description": "Işıklı tabela ile ışıksız tabela karşılaştırması. Ne zaman hangisi seçilmeli?",
        "pk": "ışıklı mı ışıksız mı",
        "primary_service": "isikli-tabela",
        "intro": "Karşılaştırma rehberi. Birincil ticari hedef ışıklı tabela hizmet sayfasındadır; bu sayfa karar destekler.",
        "sections": [
            ("Görünürlük", "Işıklı gece avantajı sağlar; ışıksız gündüz yeterli olabilir."),
            ("Maliyet", "Işıklı sistemde kasa, LED ve elektrik maliyeti eklenir."),
            ("Bakım", "LED ve güç kaynakları servis gerektirebilir."),
            ("Cephe tipi", "Mimari ve izinler seçimi etkiler."),
        ],
        "mistakes": [
            "Gece kapalı işletmeye pahalı ışıklı sistem zorlamak",
            "Elektrik altyapısını planlamadan ışıklı seçmek",
        ],
        "faqs": [
            ("LED tabela neon mu?", "Hayır. Neon ayrı formdur."),
            ("Lightbox aynı şey mi?", "Hayır. Lightbox ayrı ürün dilidir."),
        ],
    },
    {
        "slug": "kutu-harf-malzemeler",
        "title": "Kutu Harf Malzemeleri: Pleksi mi Paslanmaz mı?",
        "description": "Kutu harf malzeme karşılaştırması: pleksi/akrilik ve paslanmaz seçenekleri.",
        "pk": "kutu harf malzemeleri",
        "primary_service": "kutu-harf",
        "intro": "Malzeme karşılaştırması bilgilendirme sayfasıdır. Satın alma niyeti kutu harf hizmet sayfasındadır.",
        "sections": [
            ("Pleksi / akrilik", "Işıklı harflerde yaygın; renk ve ışık geçirgenliği avantajı."),
            ("Paslanmaz", "Prestij ve dış dayanım; bütçe daha yüksektir."),
            ("Işıklı vs ışıksız harf", "Gece okunurluk ihtiyacına göre."),
            ("Montaj yüzeyi", "Kompozit, beton, cam — keşif şart."),
        ],
        "mistakes": [
            "Channel letters için ayrı URL aramak (aynı aile)",
            "Font dosyasız üretim beklemek",
        ],
        "faqs": [
            ("Channel letters nedir?", "Kutu harfin uluslararası adıdır."),
            ("Hangisi daha uzun ömürlü?", "Koşula göre değişir; paslanmaz dış ortamda sık tercih edilir."),
        ],
    },
    {
        "slug": "one-way-vision-nedir",
        "title": "One Way Vision Nedir?",
        "description": "One way vision nedir, nerede kullanılır, avantajları nelerdir?",
        "pk": "one way vision nedir",
        "primary_service": "cam-giydirme",
        "intro": "Tanım ve kullanım rehberi. Ticari uygulama cam giydirme hizmet sayfasındadır.",
        "sections": [
            ("Nasıl çalışır?", "Dışarıdan grafik, içeriden görüş sağlayan delikli folyo."),
            ("Nerede kullanılır?", "Mağaza vitrini, showroom, araç camı (bağlama göre)."),
            ("Alternatifler", "Transparan baskı, kumlama folyo, tam kapalı folyo."),
            ("Bakım", "Kenar kalkması ve temizlik ürünlerine dikkat."),
        ],
        "mistakes": [
            "İç görüş ihtiyacı varken opak folyo seçmek",
            "Cam ölçüsüz sipariş",
        ],
        "faqs": [
            ("Araç camında olur mu?", "Uygulamaya göre; araç giydirme kapsamında değerlendirilir."),
            ("Ne kadar dayanır?", "Folyo kalitesi ve güneş/yıkama koşullarına bağlıdır."),
        ],
    },
    {
        "slug": "arac-giydirme-rehberi",
        "title": "Araç Giydirme Rehberi: Süreç, Ömür, Filo",
        "description": "Araç giydirme süreci, folyo ömrü ve filo uygulamaları hakkında rehber.",
        "pk": "araç giydirme süreci",
        "primary_service": "arac-giydirme",
        "intro": "Eğitimsel rehber. Fiyat / sipariş niyeti araç giydirme hizmet ve Tekirdağ S×C sayfalarındadır.",
        "sections": [
            ("Süreç", "Ölçü → tasarım → baskı → uygulama."),
            ("Full vs parça", "Bütçe ve marka alanına göre."),
            ("Filo standardı", "Aynı şablonun araç tipine uyarlanması."),
            ("Ömür", "Folyo tipi, yıkama ve güneş maruziyeti."),
        ],
        "mistakes": [
            "Boya problemi olan yüzeye zorla uygulama",
            "Laminasyonsuz uzun ömür beklemek (koşula göre)",
        ],
        "faqs": [
            ("Sökerken boya gider mi?", "Doğru folyo ve uygulamada kontrollü söküm hedeflenir."),
            ("Kaç günde biter?", "Araç tipine göre; keşifte netlenir."),
        ],
    },
    {
        "slug": "tabela-fiyati",
        "title": "Tabela Fiyatını Neler Etkiler?",
        "description": "Tabela fiyatını etkileyen faktörler: ölçü, malzeme, ışıklı tercih, montaj.",
        "pk": "tabela fiyatını neler etkiler",
        "primary_service": "tabela",
        "intro": "Fiyat eğitimi sayfasıdır. Sabit fiyat listesi yayınlanmaz; teklif WhatsApp / telefon ile alınır. Geo fiyat aramaları ilgili S×C sayfalarının fiyat modüllerine aittir.",
        "sections": [
            ("Ölçü ve alan", "m² ve harf yüksekliği temel çarpandır."),
            ("Malzeme", "Kompozit, pleksi, paslanmaz farklı maliyetler."),
            ("Işık", "LED, trafo, kasa derinliği."),
            ("Montaj", "Yükseklik, vinç, saha zorluğu."),
            ("Adet / filo / zincir", "Kurumsal toplu işlerde birim maliyet değişir."),
        ],
        "mistakes": [
            "İnternetten kopya fiyatı gerçek teklif sanmak",
            "Keşifsiz net fiyat beklemek",
        ],
        "faqs": [
            ("Hazır fiyat listeniz var mı?", "Hayır. Keşif sonrası net teklif verilir."),
            ("Tekirdağ fiyatı ayrı mı?", "Lojistik genelde üs içindir; çevre sahalar teklife yansır."),
        ],
    },
    {
        "slug": "totem-secim-rehberi",
        "title": "Totem Tabela Seçim Rehberi",
        "description": "Totem tabela nasıl seçilir? Yükseklik, ışıklı tercih ve montaj kriterleri.",
        "pk": "totem tabela nasıl seçilir",
        "primary_service": "totem",
        "intro": "Totem seçim rehberi. Pylon / monument aynı ailede anlatılır; ayrı doorway URL açılmaz.",
        "sections": [
            ("Konum", "Yol kenarı, tesis girişi, otopark."),
            ("Yükseklik ve okuma mesafesi", "Hız ve görüş açısı."),
            ("Işıklı tercih", "Gece yaklaşım ihtiyacı."),
            ("Temel / montaj", "Statik ve saha koşulları."),
        ],
        "mistakes": [
            "İç mekân display totem ile dış mekân totemi karıştırmak",
            "İzinsiz / keşifsiz yüksek sistem planlamak",
        ],
        "faqs": [
            ("Pylon nedir?", "Genelde daha yüksek yol kenarı sistem; bu sitede totem ailesinde."),
            ("OSB’ye uygun mu?", "Evet; sanayi dikeyiyle birlikte planlanır."),
        ],
    },
]


def wa(msg: str) -> str:
    return f"https://wa.me/{WA}?text={quote(msg)}"


def logo() -> str:
    return (
        '<img class="logo-mark" src="/images/logo.svg" width="120" height="19" '
        'alt="Malt Studio">'
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
    svc = "\n".join(
        f'<li><a href="/hizmetler/{s}/">{n}</a></li>' for s, n in SERVICES.items()
    )
    return f"""<footer>
  <div class="wrap">
    <div class="footer-top">
      <div>
        <div class="footer-logo">{logo()}</div>
        <p style="font-size:14px;line-height:1.6;color:rgba(241,238,231,0.65);max-width:280px;">
          Wave A1: projeler, sektörler ve bilgi katmanı. A0 para sayfalarına kanıt ve bağlam taşır.
        </p>
      </div>
      <div>
        <h4>Hizmetler (A0)</h4>
        <ul>{svc}</ul>
      </div>
      <div>
        <h4>A1 Katmanlar</h4>
        <ul>
          <li><a href="/projeler/">Projeler</a></li>
          <li><a href="/sektorler/">Sektörler</a></li>
          <li><a href="/bilgi/">Bilgi</a></li>
          <li><a href="/bolgeler/tekirdag/">Tekirdağ</a></li>
        </ul>
      </div>
      <div>
        <h4>İletişim</h4>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Tekirdağ, Türkiye</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2025–2026 Malt Studio</span>
      <span>Wave A1</span>
    </div>
  </div>
</footer>
<a class="whatsapp-btn" href="{wa("Merhaba, proje / sektör hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
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


def service_cards(slugs: list[str]) -> str:
    cards = []
    for s in slugs:
        name = SERVICES[s]
        cards.append(
            f'<a class="card" href="/hizmetler/{s}/"><h3>{name}</h3>'
            f"<p>İlgili hizmet sayfası (A0 owner).</p>"
            f'<span class="meta">Hizmet</span></a>'
        )
    return "\n".join(cards)


def project_cards(slugs: list[str] | None = None) -> str:
    items = PROJECTS if slugs is None else [p for p in PROJECTS if p["slug"] in slugs]
    return "\n".join(
        f'<a class="card" href="/projeler/{p["slug"]}/"><h3>{p["name"]}</h3>'
        f'<p>{p["city"]} · {p["problem"][:80]}…</p>'
        f'<span class="meta">Proje</span></a>'
        for p in items
    )


def build_projeler_hub() -> None:
    canonical = f"{SITE}/projeler/"
    html = f"""{head("Projeler | Malt Studio İş Örnekleri", "Malt Studio tabela, ışıklı tabela, kutu harf ve araç giydirme proje örnekleri.", canonical)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Projeler", None))}
    <div class="eyebrow">Wave A1 · Proof layer</div>
    <h1>Projeler</h1>
    <p class="lede">Gerçek iş kanıtı katmanı. Projeler para sayfalarına otorite taşır; kendileri geo-money H1 taşımaz.</p>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Seçili işler</h2>
    <p class="intro">Her kart bir vaka sayfasına gider. Görseller onaylandıkça eklenecektir.</p>
    <div class="card-grid">{project_cards()}</div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>Hizmetlere dön</h2>
    <div class="card-grid">{service_cards(list(SERVICES))}</div>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "projeler" / "index.html", html)


def build_project(p: dict) -> None:
    canonical = f"{SITE}/projeler/{p['slug']}/"
    svc_links = service_cards(p["services"])
    related = [x for x in PROJECTS if x["slug"] != p["slug"] and x["industry"] == p["industry"]]
    if len(related) < 2:
        related = [x for x in PROJECTS if x["slug"] != p["slug"]][:3]
    else:
        related = related[:3]
    rel_cards = project_cards([x["slug"] for x in related])
    objs = "".join(f"<li>{o}</li>" for o in p["objectives"])
    faqs = [
        (f"{p['name']} hangi hizmetleri kullandı?", ", ".join(SERVICES[s] for s in p["services"]) + "."),
        ("Bu bir satış sayfası mı?", "Hayır. Vaka / kanıt sayfasıdır. Teklif için hizmet veya WhatsApp kullanın."),
    ]
    html = f"""{head(
        f"{p['name']} Projesi | Malt Studio",
        f"{p['name']} — {p['city']} {', '.join(SERVICES[s] for s in p['services'])} uygulaması.",
        canonical,
    )}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Projeler", "/projeler/"), (p["name"], None))}
    <div class="eyebrow">Case study · Proof</div>
    <h1>{p["name"]}</h1>
    <p class="lede">{p["problem"]}</p>
    <div class="trust-strip">
      <span><strong>Şehir:</strong> {p["city"]}</span>
      <span><strong>Sektör:</strong> <a href="/sektorler/{p['industry']}/">{p['industry']}</a></span>
      <span><strong>Hizmetler:</strong> {", ".join(SERVICES[s] for s in p["services"])}</span>
    </div>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa(f"Merhaba, {p['name']} benzeri bir proje için bilgi almak istiyorum.")}" target="_blank" rel="noopener">Benzer Proje Teklifi</a>
      <a class="btn btn-ghost" href="{p['city_href']}">{p['city']}</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    <div class="content-block">
      <h2>Problem</h2>
      <p>{p["problem"]}</p>
    </div>
    <div class="content-block">
      <h2>Hedefler</h2>
      <ul>{objs}</ul>
    </div>
    <div class="content-block">
      <h2>Üretim</h2>
      <p>{p["production"]}</p>
    </div>
    <div class="content-block">
      <h2>Malzemeler</h2>
      <p>{p["materials"]}</p>
    </div>
    <div class="content-block">
      <h2>Montaj</h2>
      <p>{p["installation"]}</p>
    </div>
    <div class="content-block">
      <h2>Zorluklar</h2>
      <p>{p["challenges"]}</p>
    </div>
    <div class="content-block">
      <h2>Sonuç</h2>
      <p>{p["results"]}</p>
      <p class="note">{p["note"]}</p>
    </div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Kullanılan hizmetler</h2>
    <div class="card-grid">{svc_links}</div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>İlgili projeler</h2>
    <div class="card-grid">{rel_cards}</div>
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
    <h2>Benzer bir iş konuşalım</h2>
    <a class="btn btn-primary" href="{wa("Merhaba, benzer bir proje için keşif istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "projeler" / p["slug"] / "index.html", html)


def build_sektorler_hub() -> None:
    canonical = f"{SITE}/sektorler/"
    cards = "\n".join(
        f'<a class="card" href="/sektorler/{i["slug"]}/"><h3>{i["name"]}</h3>'
        f'<p>{i["lede"]}</p><span class="meta">Sektör</span></a>'
        for i in INDUSTRIES
    )
    html = f"""{head("Sektörler | Fabrika, Restoran, Sağlık, Plaza", "Malt Studio sektör çözümleri: fabrika/OSB, restoran, sağlık, plaza, şantiye, perakende.", canonical)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Sektörler", None))}
    <div class="eyebrow">Wave A1 · Industry layer</div>
    <h1>Sektörler</h1>
    <p class="lede">Dikey girişler. Sektör sayfaları hizmet PK’sini çalmaz; ilgili A0 hizmetlere bağlar.</p>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Sektör rehberi</h2>
    <div class="card-grid">{cards}</div>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "sektorler" / "index.html", html)


def build_industry(i: dict) -> None:
    canonical = f"{SITE}/sektorler/{i['slug']}/"
    needs = "".join(f"<li>{n}</li>" for n in i["needs"])
    proj = [p for p in PROJECTS if p["industry"] == i["slug"]]
    if proj:
        proj_section = f'<div class="card-grid">{project_cards([p["slug"] for p in proj])}</div>'
    else:
        proj_section = (
            '<p class="note">Bu dikeyde yayınlanmış proje henüz yok — '
            "eklendikçe burada listelenir.</p>"
        )
    faqs = [
        (f"{i['name']} için hangi hizmetler öne çıkar?", ", ".join(SERVICES[s] for s in i["services"]) + "."),
        ("Bu sayfa hizmet sayfasının yerine geçer mi?", "Hayır. Sektör girişidir; satın alma ilgili hizmet URL’sindedir."),
    ]
    html = f"""{head(i["title"], i["description"], canonical)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Sektörler", "/sektorler/"), (i["name"], None))}
    <div class="eyebrow">Industry · Vertical entry</div>
    <h1>{i["name"]}</h1>
    <p class="lede">{i["lede"]}</p>
    <div class="trust-strip">
      <span><strong>Owner PK:</strong> {i["pk"]} (vertical)</span>
      <span><strong>Not:</strong> bare service PK yok</span>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    <div class="content-block">
      <h2>Sektör ihtiyacı</h2>
      <p>{i["intro"]}</p>
      <ul>{needs}</ul>
      <p>{i["district_bias"]}</p>
    </div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>İlgili hizmetler</h2>
    <p class="intro">Para sayfaları A0’da yaşar.</p>
    <div class="card-grid">{service_cards(i["services"])}</div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>İlgili projeler</h2>
    {proj_section}
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Tekirdağ bağlantısı</h2>
    <div class="card-grid">
      <a class="card" href="/bolgeler/tekirdag/"><h3>Tekirdağ</h3><p>Şehir hub.</p><span class="meta">City</span></a>
      <a class="card" href="/hizmet-bolge/tekirdag-{i['services'][0]}/"><h3>Tekirdağ {SERVICES[i['services'][0]]}</h3><p>Örnek geo-money sayfa.</p><span class="meta">S×C</span></a>
      <a class="card" href="/projeler/"><h3>Tüm projeler</h3><p>Kanıt katmanı.</p><span class="meta">Projects</span></a>
    </div>
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
    <h2>{i["name"]} için keşif</h2>
    <a class="btn btn-primary" href="{wa(f"Merhaba, {i['name']} sektörü için çözüm istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "sektorler" / i["slug"] / "index.html", html)


def build_bilgi_hub() -> None:
    canonical = f"{SITE}/bilgi/"
    cards = "\n".join(
        f'<a class="card" href="/bilgi/{a["slug"]}/"><h3>{a["title"]}</h3>'
        f'<p>PK: {a["pk"]}</p><span class="meta">Rehber</span></a>'
        for a in ARTICLES
    )
    html = f"""{head("Bilgi Merkezi | Tabela ve Reklam Rehberleri", "Tabela çeşitleri, ışıklı/ışıksız karşılaştırma, kutu harf, one way vision ve fiyat rehberleri.", canonical)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Bilgi", None))}
    <div class="eyebrow">Wave A1 · Knowledge layer</div>
    <h1>Bilgi</h1>
    <p class="lede">Eğitici içerik. Money H1 taşımaz; birincil hizmet sayfalarına destek verir.</p>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Rehberler</h2>
    <div class="card-grid">{cards}</div>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "bilgi" / "index.html", html)


def build_article(a: dict) -> None:
    canonical = f"{SITE}/bilgi/{a['slug']}/"
    sections = "\n".join(
        f'<div class="content-block"><h2>{h}</h2><p>{p}</p></div>' for h, p in a["sections"]
    )
    mistakes = "".join(f"<li>{m}</li>" for m in a["mistakes"])
    svc = a["primary_service"]
    related_arts = [x for x in ARTICLES if x["slug"] != a["slug"]][:3]
    art_cards = "\n".join(
        f'<a class="card" href="/bilgi/{x["slug"]}/"><h3>{x["title"]}</h3>'
        f'<span class="meta">Devam</span></a>'
        for x in related_arts
    )
    html = f"""{head(a["title"], a["description"], canonical)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Bilgi", "/bilgi/"), (a["title"], None))}
    <div class="eyebrow">Knowledge · Informational</div>
    <h1>{a["title"]}</h1>
    <p class="lede">{a["intro"]}</p>
    <div class="trust-strip">
      <span><strong>Owner PK:</strong> {a["pk"]}</span>
      <span><strong>Feeds:</strong> /hizmetler/{svc}/</span>
      <span><strong>Not money H1</strong></span>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    <div class="content-block">
      <h2>Bu yazı ne işe yarar?</h2>
      <p>{a["intro"]}</p>
      <p class="note">Ownership: Bu sayfa “{a["pk"]}” bilgilendirme sahibidir. “{SERVICES[svc]}” ticari niyeti /hizmetler/{svc}/ sayfasındadır.</p>
    </div>
    {sections}
    <div class="content-block">
      <h2>Sık yapılan hatalar</h2>
      <ul>{mistakes}</ul>
    </div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>İlgili hizmet</h2>
    <div class="card-grid">
      <a class="card" href="/hizmetler/{svc}/"><h3>{SERVICES[svc]}</h3><p>Ticari owner sayfa.</p><span class="meta">Service</span></a>
      <a class="card" href="/hizmet-bolge/tekirdag-{svc}/"><h3>Tekirdağ {SERVICES[svc]}</h3><p>Geo-money owner.</p><span class="meta">S×C</span></a>
      <a class="card" href="/projeler/"><h3>Projeler</h3><p>Kanıt örnekleri.</p><span class="meta">Proof</span></a>
    </div>
  </div>
</section>
<section class="section-band">
  <div class="wrap">
    <h2>Sık sorulan sorular</h2>
    <div class="faq">{faq_html(a["faqs"])}</div>
  </div>
</section>
<section class="section-band paper-band">
  <div class="wrap">
    <h2>Sonraki okumalar</h2>
    <div class="card-grid">{art_cards}</div>
  </div>
</section>
<section class="cta-band">
  <div class="wrap">
    <h2>Uygulama için konuşalım</h2>
    <a class="btn btn-primary" href="{wa(f"Merhaba, {SERVICES[svc]} hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
    <a class="btn btn-ghost" href="/hizmetler/{svc}/" style="margin-left:12px;">{SERVICES[svc]} sayfası</a>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "bilgi" / a["slug"] / "index.html", html)


def merge_sitemap() -> None:
    """Rewrite sitemap with A0 + A1 URLs. Does not edit A0 HTML pages."""
    urls = [
        f"{SITE}/",
        f"{SITE}/hizmetler/",
        f"{SITE}/bolgeler/tekirdag/",
    ]
    for s in SERVICES:
        urls.append(f"{SITE}/hizmetler/{s}/")
        urls.append(f"{SITE}/hizmet-bolge/tekirdag-{s}/")
    urls += [f"{SITE}/projeler/", f"{SITE}/sektorler/", f"{SITE}/bilgi/"]
    for p in PROJECTS:
        urls.append(f"{SITE}/projeler/{p['slug']}/")
    for i in INDUSTRIES:
        urls.append(f"{SITE}/sektorler/{i['slug']}/")
    for a in ARTICLES:
        urls.append(f"{SITE}/bilgi/{a['slug']}/")

    body = "\n".join(
        f"""  <url>
    <loc>{u}</loc>
    <lastmod>2026-08-06</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if u == SITE + "/" else "0.7"}</priority>
  </url>"""
        for u in urls
    )
    (ROOT / "sitemap.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{body}
</urlset>
""",
        encoding="utf-8",
    )
    print("wrote sitemap.xml", len(urls), "urls")


def main() -> None:
    # Safety: never rewrite A0 trees
    a0_touch = [
        ROOT / "index.html",
        ROOT / "hizmetler" / "tabela" / "index.html",
        ROOT / "bolgeler" / "tekirdag" / "index.html",
        ROOT / "hizmet-bolge" / "tekirdag-tabela" / "index.html",
    ]
    before = {p: p.stat().st_mtime if p.exists() else None for p in a0_touch}

    build_projeler_hub()
    for p in PROJECTS:
        build_project(p)
    build_sektorler_hub()
    for i in INDUSTRIES:
        build_industry(i)
    build_bilgi_hub()
    for a in ARTICLES:
        build_article(a)
    merge_sitemap()

    for p, mtime in before.items():
        if p.exists() and mtime is not None and p.stat().st_mtime != mtime:
            raise SystemExit(f"ERROR: A0 page was modified: {p}")
    print("Wave A1 build complete. A0 pages untouched.")


if __name__ == "__main__":
    main()
