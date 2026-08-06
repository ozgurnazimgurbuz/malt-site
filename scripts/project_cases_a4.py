#!/usr/bin/env python3
"""Wave A4 — Unique case-study seeds for existing project URLs only."""

from __future__ import annotations

# Frozen slugs only. No invented measurements, prices, dates, or outcomes.
# Fields marked awaiting_* stay explicit until real project data arrives.

INDUSTRY_LABEL = {
    "restoran-cafe": "Restoran & Cafe",
    "fabrika-osb": "Fabrika & OSB",
    "plaza-ofis": "Plaza & Ofis",
    "perakende": "Perakende",
    "saglik": "Sağlık",
    "insaat-santiye": "İnşaat & Şantiye",
}

KNOWLEDGE_BY_SERVICE = {
    "tabela": [("/bilgi/tabela-cesitleri/", "Tabela Çeşitleri"), ("/bilgi/tabela-fiyati/", "Tabela Fiyatını Neler Etkiler?")],
    "isikli-tabela": [("/bilgi/isikli-mi-isiksiz-mi/", "Işıklı mı Işıksız mı?")],
    "kutu-harf": [("/bilgi/kutu-harf-malzemeler/", "Kutu Harf Malzemeleri")],
    "totem": [("/bilgi/totem-secim-rehberi/", "Totem Seçim Rehberi")],
    "arac-giydirme": [("/bilgi/arac-giydirme-rehberi/", "Araç Giydirme Rehberi")],
    "cam-giydirme": [("/bilgi/one-way-vision-nedir/", "One Way Vision Nedir?")],
    "ofis-branding": [("/bilgi/tabela-cesitleri/", "Tabela Çeşitleri")],
    "lightbox": [("/bilgi/isikli-mi-isiksiz-mi/", "Işıklı mı Işıksız mı?")],
    "display-pos": [("/bilgi/tabela-cesitleri/", "Tabela Çeşitleri")],
    "is-guvenligi-tabelalari": [("/bilgi/tabela-cesitleri/", "Tabela Çeşitleri")],
}

CASES = {
    "liman-kahve": {
        "name": "Liman Kahve",
        "industry": "restoran-cafe",
        "services": ["isikli-tabela", "cam-giydirme", "tabela"],
        "title": "Liman Kahve Vaka Çalışması | Cafe Tabela & Vitrin",
        "desc": "Liman Kahve için cafe cephe ve vitrin görünürlüğü vaka sayfası. Kanıt görselleri onay sonrası eklenecek.",
        "h1": "Liman Kahve",
        "lede": "Tekirdağ’da cafe işletmesi için cephe okunurluğu ve vitrin yüzeyini aynı dilde toplayan bir uygulama vakası.",
        "summary": [
            "Bu sayfa Liman Kahve işinin vaka iskeletidir. Amaç; cafe ölçeğinde tabela, ışıklı görünürlük ve cam yüzey kararlarının nasıl birlikte ele alındığını göstermektir.",
            "Müşteri onayı ve gerçek saha fotoğrafları gelene kadar ölçüm, tarih ve sonuç iddiası yazılmaz. Eksik alanlar açıkça “proje verisi bekleniyor” olarak işaretlenir.",
        ],
        "need": [
            "Cafe cephesinde gündüz/gece okunurluk ve vitrinde kampanya değişimine uygun yüzey ihtiyacı konuşulmuştur.",
            "Kesin brief maddeleri, ölçüler ve öncelik sırası: proje verisi bekleniyor.",
        ],
        "scope": [
            "Kapsam adayları: ışıklı tabela, cam giydirme ve genel tabela yüzeyi. Nihai kalem listesi onaylı iş emrine göre güncellenir.",
            "Kapsam dışı iddialar (metrekare, bütçe, süre garantisi) bu aşamada yayınlanmaz.",
        ],
        "process": [
            "Keşif ve ölçü notları → tasarım onayı → atölye üretimi → saha uygulama → teslim kontrolü.",
            "Bu projedeki gerçek takvim ve saha notları: proje verisi bekleniyor.",
        ],
        "installation": [
            "Cafe işletme saatlerine göre montaj penceresi planlanır; trafik ve vitrin erişimi keşifte kontrol edilir.",
            "Montaj günü fotoğrafları ve teslim tutanağı: proje verisi bekleniyor.",
        ],
        "materials": [
            "Aday malzeme ailesi: LED ışıklı sistem, cam folyo / OWV ve tabela paneli. Marka renkleri ve yüzey tipi onaya bağlıdır.",
            "Kesin malzeme listesi ve tedarikçi notları: proje verisi bekleniyor.",
        ],
        "technical": [
            "Teknik detaylar (ölçü, güç kaynağı, folyo tipi, montaj yüzeyi) keşif formu ile tutulur.",
            "Yayınlanabilir teknik özet: proje verisi bekleniyor.",
        ],
        "result": [
            "Hedeflenen sonuç: cafe kimliğinin cephe ve vitrinde tutarlı okunması. Nicel sonuç veya “önce/sonra” iddiası görseller olmadan yazılmaz.",
            "Sonuç kanıtı (galeri, before/after): proje verisi bekleniyor.",
        ],
        "related_projects": ["dortnal", "mera-otel", "ekip-yazilim"],
    },
    "volt-enerji": {
        "name": "Volt Enerji",
        "industry": "fabrika-osb",
        "services": ["totem", "tabela", "kutu-harf"],
        "title": "Volt Enerji Vaka Çalışması | Tesis Totem & Tabela",
        "desc": "Volt Enerji için tesis girişi ve cephe kimliği vaka sayfası. Kanıt görselleri onay sonrası eklenecek.",
        "h1": "Volt Enerji",
        "lede": "Enerji / tesis bağlamında yol yaklaşımı ve giriş kimliğini totem ve tabela ile kurgulayan sanayi vakası.",
        "summary": [
            "Volt Enerji sayfası, OSB veya tesis tipi işlerde uzaktan okunan kimlik ihtiyacını anlatmak için yapılandırılmıştır.",
            "Tesis adı portföy yer tutucusudur. Şantiye fotoğrafı, temel detayı ve onaylı ölçüler gelmeden kesin teknik iddia eklenmez.",
        ],
        "need": [
            "Yol ve kapı aksında tesisin bulunabilirliği; cephede kurumsal yazı ihtiyacı değerlendirme konusudur.",
            "Hangi yüzeylerin öncelikli olduğu ve mevcut tabela durumu: proje verisi bekleniyor.",
        ],
        "scope": [
            "Kapsam adayları: totem, tabela ve kutu harf. Vinç, temel ve izin kalemleri keşifle netleşir.",
            "Onaylı kapsam dokümanı: proje verisi bekleniyor.",
        ],
        "process": [
            "Saha keşfi (zemin/erişim) → tasarım → üretim → saha montajı → teslim.",
            "Temel ve montaj günlüğü: proje verisi bekleniyor.",
        ],
        "installation": [
            "Totem ve cephe işlerinde zemin hazırlığı, ankraj ve güvenlik mesafesi kritiktir.",
            "Kurulum fotoğrafları ve güvenlik notları: proje verisi bekleniyor.",
        ],
        "materials": [
            "Adaylar: çelik/alu totem gövde, tabela paneli, kutu harf yüzeyleri. Renk ve kaplama onaya bağlıdır.",
            "Kesin malzeme spesifikasyonu: proje verisi bekleniyor.",
        ],
        "technical": [
            "Rüzgâr yükü, temel tipi, harf derinliği ve aydınlatma ihtiyacı keşifte ayrılır.",
            "Yayınlanabilir teknik tablo: proje verisi bekleniyor.",
        ],
        "result": [
            "Hedef: tesisin yaklaşım ve girişte doğru okunması. Performans iddiası fotoğraf ve müşteri onayı sonrası yazılır.",
            "Sonuç kanıtı: proje verisi bekleniyor.",
        ],
        "related_projects": ["kuzey-tekstil", "mera-otel", "liman-kahve"],
    },
    "kuzey-tekstil": {
        "name": "Kuzey Tekstil",
        "industry": "fabrika-osb",
        "services": ["tabela", "arac-giydirme", "totem"],
        "title": "Kuzey Tekstil Vaka Çalışması | OSB Tabela & Filo",
        "desc": "Kuzey Tekstil için tesis tabela ve filo giydirme vaka sayfası. Kanıt görselleri onay sonrası eklenecek.",
        "h1": "Kuzey Tekstil",
        "lede": "Tekstil / üretim tesisi ölçeğinde sabit tabela ile hareketli filo görünürlüğünü aynı marka dilinde ele alan vaka.",
        "summary": [
            "Kuzey Tekstil, fabrika kimliği ile araç filosunun birlikte okunması gereken iş tipini temsil eder.",
            "Filo adedi, araç tipleri ve tesis cephe ölçüleri doğrulanmadan sayısal iddia yayınlanmaz.",
        ],
        "need": [
            "Tesis girişi ve saha içi yönlendirme ile filo üzeri marka görünürlüğü ihtiyacı konuşulmuştur.",
            "Öncelikli yüzeyler ve mevcut uygulamalar: proje verisi bekleniyor.",
        ],
        "scope": [
            "Kapsam adayları: tabela, totem ve araç giydirme. Filo araç listesi iş emrine bağlanır.",
            "Onaylı kapsam: proje verisi bekleniyor.",
        ],
        "process": [
            "Keşif (tesis + araç) → tasarım şablonları → üretim/baskı → montaj ve giydirme → kontrol.",
            "Gerçek süreç günlüğü: proje verisi bekleniyor.",
        ],
        "installation": [
            "Tesis montajı ile araç giydirme ayrı pencerelerde planlanabilir; filo için kuru/temiz yüzey şarttır.",
            "Uygulama fotoğrafları: proje verisi bekleniyor.",
        ],
        "materials": [
            "Adaylar: dış mekân tabela malzemeleri, totem gövde, araç cast/kalender folyo seçenekleri.",
            "Kesin malzeme ve folyo tipi: proje verisi bekleniyor.",
        ],
        "technical": [
            "Araç şablonları, tabela ölçüleri ve montaj yüzeyi teknik dosyada tutulur.",
            "Yayın özeti: proje verisi bekleniyor.",
        ],
        "result": [
            "Hedef: tesis ve filoda tutarlı marka okuması. Before/after olmadan başarı iddiası yok.",
            "Sonuç kanıtı: proje verisi bekleniyor.",
        ],
        "related_projects": ["volt-enerji", "dortnal", "ekip-yazilim"],
    },
    "mera-otel": {
        "name": "Mera Otel",
        "industry": "plaza-ofis",
        "services": ["kutu-harf", "isikli-tabela", "tabela"],
        "title": "Mera Otel Vaka Çalışması | Konaklama Kutu Harf & Tabela",
        "desc": "Mera Otel için giriş ve cephe kimliği vaka sayfası. Kanıt görselleri onay sonrası eklenecek.",
        "h1": "Mera Otel",
        "lede": "Konaklama girişinde prestij algısı ve gece okunurluğu için kutu harf / ışıklı tabela odaklı vaka iskeleti.",
        "summary": [
            "Mera Otel sayfası, misafir yaklaşımında okunan cephe kimliği ihtiyacını anlatır. Sektör bağı plaza/ofis dikeyinde tutulur; konaklama bağlamı metinde açılır.",
            "Otel logosu, cephe kısıtları ve aydınlatma kuralları onaylanmadan kesin görsel iddia eklenmez.",
        ],
        "need": [
            "Giriş aksında markanın uzaktan okunması ve gece görünürlük ihtiyacı değerlendirme konusudur.",
            "Mevcut tabela durumu ve site yönetimi kuralları: proje verisi bekleniyor.",
        ],
        "scope": [
            "Kapsam adayları: kutu harf, ışıklı tabela ve destekleyici tabela yüzeyleri.",
            "Onaylı kalem listesi: proje verisi bekleniyor.",
        ],
        "process": [
            "Keşif (cephe/elektrik) → tasarım onayı → üretim → gece testi ihtiyacına göre montaj → teslim.",
            "Gerçek süreç kayıtları: proje verisi bekleniyor.",
        ],
        "installation": [
            "Yükseklik, iskele/vinç ve misafir trafiği montaj penceresini belirler.",
            "Kurulum kanıtı: proje verisi bekleniyor.",
        ],
        "materials": [
            "Adaylar: pleksi/paslanmaz kutu harf, LED ışıklı kasa, cepheye uygun tabela paneli.",
            "Kesin malzeme seçimi: proje verisi bekleniyor.",
        ],
        "technical": [
            "Harf derinliği, LED tipi ve bağlantı detayı teknik dosyada tutulur.",
            "Yayınlanabilir teknik özet: proje verisi bekleniyor.",
        ],
        "result": [
            "Hedef: giriş kimliğinin gündüz ve gece tutarlı okunması. Kanıt görselleri şarttır.",
            "Sonuç kanıtı: proje verisi bekleniyor.",
        ],
        "related_projects": ["liman-kahve", "ekip-yazilim", "volt-enerji"],
    },
    "dortnal": {
        "name": "Dörtnal",
        "industry": "perakende",
        "services": ["isikli-tabela", "cam-giydirme", "tabela"],
        "title": "Dörtnal Vaka Çalışması | Mağaza Tabela & Vitrin",
        "desc": "Dörtnal için perakende mağaza cephe ve vitrin vaka sayfası. Kanıt görselleri onay sonrası eklenecek.",
        "h1": "Dörtnal",
        "lede": "Perakende vitrin ve cephede hızlı okunan mağaza kimliği ile yenilenebilir cam yüzeyini birleştiren vaka.",
        "summary": [
            "Dörtnal, cadde/mağaza tipinde ışıklı okunurluk ve vitrin kampanya alanını aynı işte toplayan örnektir.",
            "Mağaza adresi, vitrin ölçüleri ve kampanya takvimi doğrulanmadan kesin iddia yazılmaz.",
        ],
        "need": [
            "Mağaza cephesinde gece görünürlük ve vitrinde değişebilir mesaj alanı ihtiyacı konuşulmuştur.",
            "Mevcut yüzey durumu: proje verisi bekleniyor.",
        ],
        "scope": [
            "Kapsam adayları: ışıklı tabela, cam giydirme ve tabela. Kampanya baskı adetleri ayrıca tanımlanır.",
            "Onaylı kapsam: proje verisi bekleniyor.",
        ],
        "process": [
            "Keşif → tasarım → üretim/baskı → montaj ve folyo uygulama → teslim.",
            "Saha günlüğü: proje verisi bekleniyor.",
        ],
        "installation": [
            "Vitrin temizliği, folyo uygulaması ve tabela montajı işletme saatlerine göre planlanır.",
            "Uygulama fotoğrafları: proje verisi bekleniyor.",
        ],
        "materials": [
            "Adaylar: LED tabela bileşenleri, OWV/folyo, tabela paneli.",
            "Kesin malzeme: proje verisi bekleniyor.",
        ],
        "technical": [
            "Vitrin cam tipi, folyo yönü ve tabela bağlantısı teknik notlara işlenir.",
            "Yayın özeti: proje verisi bekleniyor.",
        ],
        "result": [
            "Hedef: mağazanın cadde kotunda net okunması ve vitrinin güncellenebilir olması.",
            "Sonuç kanıtı: proje verisi bekleniyor.",
        ],
        "related_projects": ["liman-kahve", "kuzey-tekstil", "mera-otel"],
    },
    "ekip-yazilim": {
        "name": "Ekip Yazılım",
        "industry": "plaza-ofis",
        "services": ["kutu-harf", "cam-giydirme", "ofis-branding"],
        "title": "Ekip Yazılım Vaka Çalışması | Ofis Branding & Kutu Harf",
        "desc": "Ekip Yazılım için ofis iç kimlik ve giriş uygulamaları vaka sayfası. Kanıt görselleri onay sonrası eklenecek.",
        "h1": "Ekip Yazılım",
        "lede": "Plaza / ofis katında karşılama, cam yüzey ve iç kimlik uygulamalarını bir araya getiren kurumsal vaka iskeleti.",
        "summary": [
            "Ekip Yazılım, B2B ofis ortamında markanın kapı, cam ve iç yüzeylerde tutarlı görünmesi gereken iş tipini temsil eder.",
            "Kat planı, site yönetimi kuralları ve logo dosyaları onaylanmadan kesin uygulama iddiası eklenmez.",
        ],
        "need": [
            "Ofis girişi ve cam yüzeylerde kurumsal kimlik; iç mekânda sade marka dili ihtiyacı değerlendirme konusudur.",
            "Kat/alan kısıtları: proje verisi bekleniyor.",
        ],
        "scope": [
            "Kapsam adayları: ofis branding, kutu harf ve cam giydirme.",
            "Onaylı kapsam: proje verisi bekleniyor.",
        ],
        "process": [
            "Keşif (iç mekân) → tasarım → üretim → uygulama → teslim.",
            "Gerçek süreç kayıtları: proje verisi bekleniyor.",
        ],
        "installation": [
            "Plaza çalışma saatleri ve asansör/erişim kuralları uygulama penceresini belirler.",
            "Kurulum kanıtı: proje verisi bekleniyor.",
        ],
        "materials": [
            "Adaylar: iç mekân uygun folyo/baskı, kutu harf malzemeleri, cam uygulama filmleri.",
            "Kesin malzeme: proje verisi bekleniyor.",
        ],
        "technical": [
            "Cam tipi, yapışkan seçimi ve harf montaj yüzeyi teknik dosyada tutulur.",
            "Yayın özeti: proje verisi bekleniyor.",
        ],
        "result": [
            "Hedef: ofiste tutarlı ve sade marka deneyimi. Fotoğraf onayı olmadan sonuç iddiası yok.",
            "Sonuç kanıtı: proje verisi bekleniyor.",
        ],
        "related_projects": ["mera-otel", "liman-kahve", "volt-enerji"],
    },
}
