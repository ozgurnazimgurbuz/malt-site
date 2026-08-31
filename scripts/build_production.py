#!/usr/bin/env python3
"""Upgrade all existing URLs to production depth. No new URLs."""

from __future__ import annotations

import html
import json
import sys
from datetime import datetime, timezone
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
    faq_html,
    faq_ld,
    footer,
    head,
    header,
    mid_cta,
    page_graph,
    process_steps,
    related_rail,
    article_ld,
    service_ld,
    wa,
    webpage_ld,
    website_node,
    write,
)
from project_cases_a4 import KNOWLEDGE_BY_SERVICE  # noqa: E402
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
ARTICLE_TITLES = {f"/bilgi/{s}/": t for s, t, _, _ in ARTICLES}


def article_title(href: str) -> str:
    return ARTICLE_TITLES.get(href, "Rehber")


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


def load_portfolio() -> list[dict]:
    """Real CMS portfolio items that have a slug + name. Empty fields stay unpublished."""
    data = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
    out = []
    for item in data.get("portfolio") or []:
        slug = str(item.get("slug") or "").strip().strip("/")
        name = str(item.get("name") or "").strip()
        if slug and name:
            out.append(item)
    return out


def _service_labels(raw) -> list[str]:
    labels = []
    for x in raw or []:
        if isinstance(x, str):
            v = x.strip()
        elif isinstance(x, dict):
            v = str(x.get("service") or x.get("name") or "").strip()
        else:
            v = ""
        if v:
            labels.append(v)
    return labels


def _fold_tr(s: str) -> str:
    # İ.casefold() is not "i"; fold Turkish dotted/dotless I before compare.
    return s.replace("İ", "i").replace("I", "i").replace("ı", "i").casefold().strip()


def _service_slug(label: str) -> str | None:
    key = _fold_tr(label)
    aliases = {
        "iş güvenliği": "is-guvenligi-tabelalari",
        "is güvenliği": "is-guvenligi-tabelalari",
        "iş güvenliği tabelaları": "is-guvenligi-tabelalari",
    }
    if key in aliases:
        return aliases[key]
    for slug, name in ALL_SERVICES.items():
        nk = _fold_tr(name)
        if nk == key or slug == key or (key and nk.startswith(key + " ")):
            return slug
    return None


def _project_images(item: dict) -> list[str]:
    seen: list[str] = []
    cover = str(item.get("image") or "").strip()
    if cover:
        seen.append(cover)
    for g in item.get("gallery") or []:
        if isinstance(g, str):
            src = g.strip()
        elif isinstance(g, dict):
            src = str(g.get("image") or g.get("src") or "").strip()
        else:
            src = ""
        if src and src not in seen:
            seen.append(src)
    return seen


def _picture(src: str, alt: str, *, lazy: bool) -> str:
    webp = ""
    lower = src.lower()
    for ext in (".jpeg", ".jpg", ".png"):
        if lower.endswith(ext):
            candidate = src[: -len(ext)] + ".webp"
            if (ROOT / candidate.lstrip("/")).is_file():
                webp = candidate
            break
    sizes = "(max-width:720px) 100vw, 780px"
    loading = ' loading="lazy"' if lazy else ""
    prio = ' fetchpriority="high"' if not lazy else ""
    decoding = ' decoding="async"' if lazy else ""
    img = (
        f'<img src="{html.escape(src)}" alt="{html.escape(alt)}" '
        f'width="800" height="1000" sizes="{sizes}"'
        f"{loading}{prio}{decoding}>"
    )
    if webp:
        return (
            f'<picture><source type="image/webp" srcset="{html.escape(webp)}" '
            f'sizes="{sizes}">{img}</picture>'
        )
    return img


def table(headers: list[str], rows: list[list[str]]) -> str:
    cell = 'style="border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top"'
    th = "".join(f"<th {cell}>{h}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td {cell}>{c}</td>" for c in row) + "</tr>" for row in rows
    )
    return (
        '<div class="table-wrap" style="overflow-x:auto;margin:1.25rem 0">'
        '<table style="width:100%;border-collapse:collapse;font-size:15px;line-height:1.5">'
        f"<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def quote_prep() -> str:
    return block(
        "Teklif öncesi ne paylaşın?",
        p("Keşif sonrası yazılı teklif çıkar. Aşağıdakiler teklifi hızlandırır; hepsi zorunlu değildir.")
        + ul(
            [
                "Cephe, cam veya araç fotoğrafı",
                "Yaklaşık ölçü veya keşif randevusu",
                "Gece görünürlük ihtiyacı (var / yok)",
                "Varsa vektörel logo veya marka kılavuzu",
            ]
        ),
    )


ARTICLE_TABLES = {
    "tabela-cesitleri": (
        "Tabela türleri nasıl ayrılır?",
        ["Tip", "Ne işe yarar", "Gece", "İlgili hizmet"],
        [
            [
                "Işıksız tabela",
                "Gündüz odaklı cephe ve iç bilgilendirme",
                "Yok / düşük",
                '<a href="/hizmetler/tabela/">Tabela</a>',
            ],
            [
                "Işıklı tabela",
                "Gece de okunan LED’li cephe sistemi",
                "Var",
                '<a href="/hizmetler/isikli-tabela/">Işıklı tabela</a>',
            ],
            [
                "Kutu harf",
                "Üç boyutlu cephe yazısı",
                "Modele göre",
                '<a href="/hizmetler/kutu-harf/">Kutu harf</a>',
            ],
            [
                "Totem",
                "Yol ve tesis yaklaşımı",
                "İhtiyaca göre",
                '<a href="/hizmetler/totem/">Totem</a>',
            ],
            [
                "Cam giydirme",
                "Vitrin mesajı, gizlilik, kampanya",
                "Hayır (aydınlatma camın içindedir)",
                '<a href="/hizmetler/cam-giydirme/">Cam giydirme</a>',
            ],
            [
                "Lightbox",
                "İç mekân / retail ışıklı kutu ve çerçeve",
                "Kutu içi ışık",
                '<a href="/hizmetler/lightbox/">Lightbox</a>',
            ],
        ],
    ),
    "isikli-mi-isiksiz-mi": (
        "Işıklı ve ışıksız tabela farkı",
        ["Kriter", "Işıklı tabela", "Işıksız tabela"],
        [
            ["Gece okunurluk", "LED ile okunur", "Gündüz odaklı; gece kaybolabilir"],
            ["Elektrik", "Hat, kasa ve güç kaynağı gerekir", "Gerekmez"],
            ["Bakım", "LED ve güç kaynağı servisi planlanır", "Yüzey, solma ve darbe kontrolü"],
            ["Tipik yer", "Gece açık mağaza, eczane, plaza girişi", "Gündüz işletme, iç yön"],
            [
                "Sipariş",
                '<a href="/hizmetler/isikli-tabela/">Işıklı tabela</a>',
                '<a href="/hizmetler/tabela/">Tabela</a>',
            ],
            [
                "Lightbox",
                "Ayrı üründür; cephe LED tabela değildir",
                "Ayrı üründür",
            ],
        ],
    ),
    "kutu-harf-malzemeler": (
        "Pleksi ve paslanmaz nasıl ayrılır?",
        ["Kriter", "Pleksi / akrilik", "Paslanmaz"],
        [
            ["Görünüm", "Renk ve ışık geçirgenliği", "Metal prestij, dış dayanım"],
            ["Işıklı kullanım", "Işıklı harfte yaygındır", "Işıklı veya ışıksız üretilebilir"],
            ["Dikkat", "Çizilme ve temizlik hassasiyeti", "Mimariye uyum; bütçe genelde daha yüksek"],
            ["Montaj", "Keşifte yüzey ve aparat netleşir", "Keşifte yüzey ve aparat netleşir"],
            [
                "Sipariş",
                '<a href="/hizmetler/kutu-harf/">Kutu harf</a>',
                '<a href="/hizmetler/kutu-harf/">Kutu harf</a>',
            ],
        ],
    ),
}


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
        "related_projects": ["ofiso", "yamanlar-ekspertiz", "pembe-pasta-evi", "anka"],
        "related_services": ["isikli-tabela", "kutu-harf", "totem", "cam-giydirme"],
        "bilgi": ["/bilgi/tabela-cesitleri/", "/bilgi/tabela-fiyati/"],
        "faqs": [
            ("Tabela ile ışıklı tabela farkı nedir?", 'Işıklı tabela gece görünürlük için LED’li sistemdir. Ayrı sayfa: <a href="/hizmetler/isikli-tabela/">ışıklı tabela</a>. Bu sayfa genel tabela üretimini kapsar.'),
            ("Montajı siz yapıyor musunuz?", "Evet. Üretim atölyede, montaj sahada birlikte planlanır."),
            ("Fiyat listesi var mı?", "Hayır. Ölçü, malzeme ve montaj keşiften sonra yazılı netleşir. Sabit internet fiyatı yayınlanmaz."),
            ("Tekirdağ dışında çalışıyor musunuz?", 'Tekirdağ üssünden çevre ilçelere keşif ve montaj planlanır. Atölye: <a href="/bolgeler/tekirdag/">Tekirdağ iletişim</a>.'),
            ("Ne kadar sürer?", "Onay ve ölçüye göre birkaç iş gününden birkaç haftaya değişir. Süre teklifte yazılır; tutulmayan süre vaadi yoktur."),
            ("Tasarım desteği var mı?", "Marka dosyanız yoksa sade ve okunur tasarım önerisi sunulur. Vektörel logo kaliteyi yükseltir."),
            ("Eski tabela sökümü?", "Yenileme işlerinde söküm ve yüzey rötuşu planlanabilir; peşin dahil varsayılmaz."),
            ("Garanti?", "Malzeme ve işçilik kapsamı teklifte yazılı netleştirilir. Peşin ‘ömür boyu’ vaadi yoktur."),
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
        "related_projects": ["kosem-doner"],
        "related_services": ["tabela", "lightbox", "kutu-harf", "cam-giydirme"],
        "bilgi": ["/bilgi/isikli-mi-isiksiz-mi/", "/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("LED tabela neon mu?", "Hayır. Neon ayrı formdur. Bu sayfadaki ışıklı tabela LED kasa sistemidir."),
            ("Lightbox istiyorum?", 'Lightbox ayrı üründür: <a href="/hizmetler/lightbox/">lightbox</a>. Cephe LED tabela bu sayfadadır.'),
            ("Elektrik hazır değilse?", "Keşifte altyapı ihtiyacı konuşulur. Hat yoksa teklife altyapı kalemi yazılır."),
            ("Servis ve arıza?", "LED ve güç kaynağı servisi için iletişime geçilir. Peşin ömür boyu vaadi yoktur."),
            ("Fiyatı neye göre?", "Ölçü, LED, yüzey ve montaj koşulları. Sabit liste yoktur; keşif sonrası yazılı teklif."),
            ("Su ve toz?", "Dış mekân kasalarında sızdırmazlık planı keşifte konuşulur."),
            ("Gece çok mu parlak olur?", "LED yoğunluğu cepheye göre ayarlanır; aşırı parlaklık okunurluğu bozar."),
            ("Süre?", "Onay sonrası ölçeğe göre netlenir ve teklifte yazılır."),
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
        "related_projects": ["kosem-doner", "okka-tarim"],
        "related_services": ["ofis-branding", "isikli-tabela", "tabela", "lightbox"],
        "bilgi": ["/bilgi/kutu-harf-malzemeler/", "/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("Pleksi mi paslanmaz mı?", 'Bütçe, mimari ve bakım beklentisine göre değişir. Karşılaştırma: <a href="/bilgi/kutu-harf-malzemeler/">kutu harf malzemeleri</a>.'),
            ("Channel letters nedir?", "Kutu harfin uluslararası adıdır. Ayrı URL yoktur; üretim bu sayfadadır."),
            ("Işıklı olur mu?", "Evet, modele göre LED’li üretilir. Işıklı/ışıksız tercih üretimden önce netleşir."),
            ("Font şart mı?", "Vektörel logo veya font dosyası kaliteyi yükseltir. Font lisansı müşteri sorumluluğundadır."),
            ("Montaj her yüzeye olur mu?", "Hayır. Kompozit, beton ve cam farklı aparat ister; keşif şarttır."),
            ("Bakım?", "Dış ortamda periyodik kontrol önerilir. Işıklı harflerde servis erişimi korunmalıdır."),
            ("Süre?", "Harf adedi ve malzemeye göre değişir; teklifte yazılır."),
            ("Ofis içi logo?", 'Ofis içi 3D logo <a href="/hizmetler/ofis-branding/">ofis branding</a> paketiyle birlikte planlanabilir.'),
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
            'Taşınabilir indoor display totem <a href="/hizmetler/display-pos/">Display & POS</a> ailesindedir.',
            "Yükseklik, temel, ışıklı tercih ve görüş mesafesi keşifte hesaplanır.",
            "Tekirdağ tesis ve OSB girişlerinde keşif sonrası temel ve yükseklik netleşir.",
        ],
        "apps": ["Fabrika/OSB girişi", "Plaza yaklaşımı", "Yol kenarı", "Otopark", "Kurumsal kampüs"],
        "materials": "Çelik/alüminyum konstrüksiyon, kompozit yüzey, ışıklı kasa seçenekleri.",
        "related_projects": ["yamanlar-ekspertiz"],
        "related_services": ["tabela", "is-guvenligi-tabelalari", "kutu-harf", "display-pos"],
        "bilgi": ["/bilgi/totem-secim-rehberi/", "/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("Totem ile pylon farkı?", "Pylon genelde daha yüksek yol sistemidir. Aynı ailede ele alınır; ayrı doorway URL açılmaz."),
            ("İzin gerekir mi?", "Konuma göre değişir. İzin riski keşifte konuşulur; süre garanti edilmez."),
            ("Işıklı totem?", "Evet, gece yaklaşım için ışıklı üretilebilir. LED servis erişimi tasarımda bırakılır."),
            ("Temel kim yapar?", "Saha planına göre koordinasyon sağlanır. Temel tipi zemin koşullarına bağlıdır."),
            ("Indoor totem?", 'Taşınabilir indoor display <a href="/hizmetler/display-pos/">Display & POS</a> ailesindedir. Bu sayfa outdoor tesis/yol totemidir.'),
            ("OSB montajı?", "Evet, planlı keşif ile. Vinç ve güvenlik penceresi keşif notuna yazılır."),
            ("Süre?", "Temel ve üretime bağlıdır. Temel kürü takvime yazılır."),
            ("Bakım?", "Bağlantı ve yüzey kontrolü önerilir. Işıklıysa LED servis erişimi korunmalıdır."),
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
        "related_projects": [],
        "related_services": ["tabela", "cam-giydirme", "display-pos", "ofis-branding"],
        "bilgi": ["/bilgi/arac-giydirme-rehberi/"],
        "faqs": [
            ("Boya zarar görür mü?", "Doğru folyo ve uygulamada kontrollü söküm hedeflenir. Araç boyasının durumu sonucu etkiler; peşin ‘boya bozulmaz’ garantisi verilmez."),
            ("Full mu parça mı?", "Bütçe ve görünür alana göre. Parça giydirme çoğu filoda yeterlidir; full wrap zorunlu değildir."),
            ("Filo indirimi?", "Toplu işlerde kurumsal teklif hazırlanır. Peşin oran ilan edilmez."),
            ("Süre?", "Tek araçta genelde kısa; filoda planlı takvim. Ortam sıcaklığı uygun değilse iş ertelenir."),
            ("Cam giydirme ayrı mı?", 'Araç camı bu kapsamdadır. Bina camı <a href="/hizmetler/cam-giydirme/">cam giydirme</a> sayfasındadır.'),
            ("Tasarım?", "Marka kılavuzuna göre uyarlanır. Araç listesi ve fotoğraf olmadan şablon çıkmaz."),
            ("Kışın uygulanır mı?", "Ortam sıcaklığı uygunsa. Uygun değilse iş ertelenir; kalitesiz yapışma riski alınmaz."),
            ("Ömür?", "Folyo tipi, yıkama, güneş ve kullanıma bağlıdır. Sayısal ömür vaadi verilmez."),
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
        "related_projects": ["ofiso", "pembe-pasta-evi"],
        "related_services": ["isikli-tabela", "ofis-branding", "tabela", "display-pos"],
        "bilgi": ["/bilgi/one-way-vision-nedir/"],
        "faqs": [
            ("One way vision nedir?", 'Dışarıdan grafik görünen, içeriden bakışa izin veren delikli folyodur. Rehber: <a href="/bilgi/one-way-vision-nedir/">one way vision nedir</a>.'),
            ("İçerisi kararır mı?", "Folyo tipine ve delik oranına göre ışık geçirgenliği değişir. Karanlık mağazada görüş zayıflayabilir."),
            ("Araç camı?", 'Araç camı <a href="/hizmetler/arac-giydirme/">araç giydirme</a> kapsamında değerlendirilir.'),
            ("Sökülür mü?", "Kampanya sonunda kontrollü söküm planlanır. Kirli cama uygulama kenar/hava hatası yapar."),
            ("Buğu / yapışma?", "Cam hazırlığı ve doğru gergi kritiktir."),
            ("Ofis paketi?", 'Ofis gizlilik folyosu <a href="/hizmetler/ofis-branding/">ofis branding</a> paketiyle birlikte yönetilebilir; malzeme bilgisi bu sayfadadır.'),
            ("Süre?", "Çoğu vitrin işi kısa sürer; ölçü ve katman sayısına göre netlenir."),
            ("Tasarım?", "Mesaj hiyerarşisi okunur tutulur. Aşırı kalabalık vitrin grafiği ürün yerine gürültü üretir."),
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
            'Işıklı tabela / LED cephe sistemleri ayrı sayfadadır: <a href="/hizmetler/isikli-tabela/">ışıklı tabela</a>. Bu sayfa lightbox ailesidir.',
            "SEG / backlit fabric hızlı görsel değişimi sağlar.",
            "Yerel talep Tekirdağ üssünden keşif ile yönetilir.",
            "Ofis ve resepsiyon duvarlarında lightbox + ofis branding birlikte planlanabilir.",
        ],
        "apps": ["Mağaza içi", "AVM", "Showroom", "Klinik bekleme", "Resepsiyon duvarı"],
        "materials": "Alüminyum kasa, LED, backlit fabric, SEG, akrilik yüz.",
        "related_projects": [],
        "related_services": ["isikli-tabela", "display-pos", "ofis-branding", "cam-giydirme"],
        "bilgi": ["/bilgi/isikli-mi-isiksiz-mi/"],
        "faqs": [
            ("Işıklı tabeladan farkı?", 'Cephe LED tabela <a href="/hizmetler/isikli-tabela/">ışıklı tabela</a> sayfasındadır. Bu sayfa lightbox kutu ve çerçeve ailesidir.'),
            ("SEG nedir?", "Silikon kenarlı kumaş germe sistemidir. Görsel değişim sıklığı yüksekse avantaj sağlar."),
            ("Görsel değişir mi?", "SEG’de hızlı kumaş değişimi mümkündür. LED değişimi ayrı kalemdir."),
            ("İnce kasa?", "Mekâna göre kasa tipi seçilir. İnce görünüm elektrik ve soğutma ile dengelenir."),
            ("Servis?", "LED ve kumaş değişimi planlanır. Servis kapsamı teklifte yazılır."),
            ("Süre?", "Ölçü ve kasa tipine göre netlenir."),
            ("Fiyat?", "Ölçü, kasa ve baskı. Sabit liste yoktur."),
            ("Tekirdağ’da keşif?", 'Evet. Keşif <a href="/bolgeler/tekirdag/">Tekirdağ atölyesinden</a> planlanır.'),
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
        "related_projects": [],
        "related_services": ["lightbox", "tabela", "cam-giydirme", "ofis-branding"],
        "bilgi": ["/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("Roll-up vs X-banner?", "Roll-up kasalı sistemdir; X-banner daha ekonomik ve daha hassas taşınır. Seçim kullanım süresine göre yapılır."),
            ("Fuar standı?", "Tekil display burada planlanır. Tam fuar standı veya backdrop ayrıca değerlendirilir."),
            ("Indoor totem?", 'Taşınabilir indoor display bu ailededir. Yol ve tesis totemi <a href="/hizmetler/totem/">totem</a> sayfasındadır.'),
            ("Adet avantajı?", "Toplu siparişte teklif özeldir. Peşin birim oran ilan edilmez."),
            ("Baskı kalitesi?", "Okunur mesafe ve çözünürlük planlanır. Onaylı görsel olmadan baskı başlamaz."),
            ("Teslimat?", "Donanım ve baskı birlikte teslim edilebilir."),
            ("Süre?", "Genelde kısa döngü; adet ve baskı tipine göre netlenir."),
            ("Yeniden baskı?", "Aynı kasaya yeni baskı yapılabilir. Kampanya yenilemesi için kasa saklanır."),
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
            "Genel duvar/zemin giydirme (her mekân) ayrı aile olarak ileride açılabilir; bu sayfa ofis paketini sahiplenir.",
            "Cam folyo uygulamaları cam giydirme uzmanlığıyla bağlanır.",
            "Plaza teslimatlarında mesaiye duyarlı montaj planlanır.",
            "Kutu harf / 3D logo sık tamamlayıcıdır.",
        ],
        "apps": ["Plaza ofisleri", "Resepsiyon", "Lobi", "Toplantı odası", "Kat kimliği"],
        "materials": "Kutu harf, cam folyo, duvar grafiği, kapı/oda isimliği (pakete göre).",
        "related_projects": ["okka-tarim"],
        "related_services": ["kutu-harf", "cam-giydirme", "lightbox", "tabela"],
        "bilgi": ["/bilgi/kutu-harf-malzemeler/"],
        "faqs": [
            ("Kapı isimliği dahil mi?", "Pakete eklenebilir. Standart set varsayılmaz; brief’te netleştirilir."),
            ("Cam giydirme ayrı mı?", 'Malzeme ve uygulama <a href="/hizmetler/cam-giydirme/">cam giydirme</a> uzmanlığıyla bağlanır; ofis paketi bu sayfadadır.'),
            ("İç mekan giydirme farkı?", "Bu sayfa workplace paketidir: resepsiyon, lobi, toplantı, kat kimliği. Her mekân duvar giydirmesi ayrı aile olarak açılmaz."),
            ("Kesinti olur mu?", "Mesai dışı veya düşük yoğunluklu pencere planlanabilir. Plaza kuralları keşifte sorulur."),
            ("Logo dosyası?", "Vektörel tercih edilir. Font lisansı müşteri sorumluluğundadır."),
            ("Süre?", "Alan büyüklüğüne ve onay süresine göre. Yönetim onayı gecikirse takvim kayar."),
            ("Plaza yönetimi onayı?", "Gerekirse keşifte konuşulur. Onaysız cephe işi risklidir."),
            ("Fiyat?", "Alan, malzeme ve erişim. Sabit liste yoktur."),
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
        "related_projects": ["anka"],
        "related_services": ["tabela", "totem", "display-pos", "ofis-branding"],
        "bilgi": ["/bilgi/tabela-cesitleri/"],
        "faqs": [
            ("Yangın çıkışı burada mı?", "Evet. Yangın çıkışı, acil çıkış ve toplanma alanı bu ailededir."),
            ("Yönlendirme aynı mı?", "Hayır. Oda/kat wayfinding bu ailenin H1’i değildir; iş güvenliği uyarı setidir."),
            ("ISO belgesi veriyor musunuz?", "Hayır. Malt Studio tabela üretir ve tedarik eder; belgelendirme kuruluşu değildir."),
            ("Toplu set?", "Listeye veya Excel’e göre üretilir. Toplu saha etiketleme OSB ve depoda sık istenir."),
            ("Dış mekân dayanım?", "Malzeme sahaya göre seçilir. UV ve darbe ihtiyacı keşifte konuşulur."),
            ("Montaj?", "Saha planıyla yapılır. Üretim hattı duruşu varsa takvim ona göre yazılır."),
            ("Süre?", "Standart setlerde hızlıdır; özel metin onayına bağlıdır."),
            ("Özel uyarı metni?", "Evet, onaya göre. Tıbbi veya yasal danışmanlık yerine geçmez."),
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
    knowledge = [(b, article_title(b), "Karar rehberi.") for b in s["bilgi"]]
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
        body_blocks = intro + choice + proof + price + process + quote_prep() + local_extra
    else:
        body_blocks = (
            block("Bu hizmet nedir?", p(*s["extra"], *a5["intro"]))
            + block("Nerelerde kullanılır?", ul(s["apps"]) + p(*a5["where"]))
            + block("Malzeme ve seçenekler", p(s["materials"], *a5["materials_extra"]))
            + quote_prep()
            + service_process()
            + block("Süreç notları", p(*a5["process_extra"]))
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
        website_node(),
        service_ld(canonical, s["h1"], s.get("service_type") or s["h1"]),
        breadcrumb_ld(
            [
                ("Ana Sayfa", "/"),
                ("Hizmetler", "/hizmetler/"),
                (s["h1"], canonical),
            ]
        ),
        faq_ld(canonical, s["faqs"]),
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
    knowledge=[(b, article_title(b), "Karar rehberi.") for b in s["bilgi"]],
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
    cms = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
    maps = (cms.get("googleMapsUrl") or "").strip().replace("&", "&amp;").replace('"', "&quot;")
    ig = (cms.get("instagram") or "").strip().replace("&", "&amp;").replace('"', "&quot;")
    svc = cards([(f"/hizmetler/{s}/", n, f"{n} hizmeti.", "Hizmet") for s, n in ALL_SERVICES.items()])
    maps_p = (
        f'Yol tarifi: <a href="{maps}" rel="noopener noreferrer" target="_blank">Google Haritalar’da koordinat araması</a>. Bu bir Place ID veya işletme profili kaydı iddiası değildir.'
        if maps
        else "Yol tarifi için Google Haritalar’da adresi arayın."
    )
    ig_p = (
        f'Instagram: <a href="{ig}" rel="noopener noreferrer" target="_blank">@maltstudio.co</a>.'
        if ig
        else ""
    )
    faqs = [
        ("Atölye nerede?", f"{ADDRESS_ONE_LINE}."),
        ("Çalışma saatleri?", HOURS_DISPLAY + "."),
        ("Süleymanpaşa ayrı sayfa mı?", "Hayır; Süleymanpaşa talepleri bu atölye sayfasında toplanır."),
        ("Keşif nasıl alınır?", "WhatsApp veya telefon ile kısa brief bırakın. Keşif sonrası yazılı teklif çıkar."),
        (
            "Hangi hizmetler Tekirdağ’dan planlanır?",
            'Tabela, ışıklı tabela, kutu harf, totem, cam ve araç giydirme, lightbox, display, ofis branding ve iş güvenliği tabelaları. Liste: <a href="/hizmetler/">hizmetler</a>.',
        ),
        ("Çevre ilçelere geliyor musunuz?", "Süleymanpaşa ve Tekirdağ merkez başta olmak üzere çevre ilçe işleri aynı atölyeden planlanır."),
    ]
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        breadcrumb_ld([("Ana Sayfa", "/"), (title, canonical)]),
        faq_ld(canonical, faqs),
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
        ig_p,
        'WhatsApp veya telefon ile keşif randevusu alınır.',
    ))}
    {block("Ulaşım", p(
        "Atölye Süleymanpaşa / Tekirdağ’dadır. Keşif randevusu sonrası ölçü ve montaj planı çıkarılır.",
        maps_p,
    ))}
    {block("Hizmet bölgeleri", p(
        "Süleymanpaşa ve Tekirdağ merkez başta olmak üzere çevre ilçelere keşif ve montaj planlanır.",
        "Çorlu, Çerkezköy, Kapaklı, Ergene, Muratlı ve diğer ilçe işleri aynı atölyeden yönetilir.",
        'Tüm hizmet listesi: <a href="/hizmetler/">hizmetler</a>.',
    ))}
    {block("Gerçek işler", p(
        'Ana sayfadaki <a href="/#isler">seçili işler</a> gerçek saha fotoğraflarıdır.',
        'Hizmet sayfaları: <a href="/hizmetler/tabela/">tabela</a>, <a href="/hizmetler/isikli-tabela/">ışıklı tabela</a>, <a href="/hizmetler/kutu-harf/">kutu harf</a>, <a href="/hizmetler/totem/">totem</a>, <a href="/hizmetler/cam-giydirme/">cam giydirme</a>, <a href="/hizmetler/arac-giydirme/">araç giydirme</a>.',
        'Rehberler: <a href="/bilgi/">bilgi merkezi</a>.',
    ))}
    {mid_cta("Tekirdağ keşif")}
  </div>
</section>
{related_rail(
    knowledge=[(f"/bilgi/{s}/", t, "Karar rehberi.") for s, t, _, _ in ARTICLES],
    industries=[(f"/sektorler/{s}/", n, f"{n} çözümleri.") for s, n, _ in INDUSTRIES],
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
    canonical = f"{SITE}/hizmetler/"
    title = "Hizmetler | Tabela, Lightbox, Ofis Branding ve Daha Fazlası"
    desc = "Malt Studio tüm hizmetleri: tabela, ışıklı tabela, kutu harf, totem, araç ve cam giydirme, lightbox, display, ofis branding, İSG."
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        breadcrumb_ld([("Ana Sayfa", "/"), ("Hizmetler", canonical)]),
    )
    html = f"""{head(title, desc, canonical, json_ld=json_ld)}
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
        'Tekirdağ atölye, saat ve adres: <a href="/bolgeler/tekirdag/">atölye ve iletişim</a>.',
    ))}
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


def build_project(item: dict) -> None:
    """Indexable case page from CMS portfolio. Renders only fields that have values."""
    slug = str(item.get("slug") or "").strip().strip("/")
    name = str(item.get("name") or "").strip()
    if not slug or not name:
        return
    canonical = f"{SITE}/projeler/{slug}/"
    title = f"{name} Projesi | Malt Studio"
    safe_name = html.escape(name)
    labels = _service_labels(item.get("services"))
    resolved = []
    for label in labels:
        s = _service_slug(label)
        resolved.append((label, s))
    known = [(label, s) for label, s in resolved if s]
    desc = (
        f"{name} için Malt Studio tarafından gerçekleştirilen uygulama projesi. "
        "Proje fotoğraflarını ve ilgili hizmet detaylarını inceleyin."
    )
    location = str(item.get("location") or "").strip()
    category = str(item.get("category") or "").strip()
    description = str(item.get("description") or "").strip()
    year = str(item.get("year") or "").strip()
    completed = str(item.get("completedDate") or "").strip()
    client = str(item.get("client") or "").strip()
    images = _project_images(item)

    meta_bits = []
    if client:
        meta_bits.append(f"<div><dt>Müşteri</dt><dd>{html.escape(client)}</dd></div>")
    if location:
        loc = html.escape(location)
        if location.casefold() in {"tekirdağ", "tekirdag"}:
            loc = f'<a href="/bolgeler/tekirdag/">{loc}</a>'
        meta_bits.append(f"<div><dt>Konum</dt><dd>{loc}</dd></div>")
    if category:
        meta_bits.append(f"<div><dt>Kategori</dt><dd>{html.escape(category)}</dd></div>")
    if year:
        meta_bits.append(f"<div><dt>Yıl</dt><dd>{html.escape(year)}</dd></div>")
    if completed:
        meta_bits.append(f"<div><dt>Tarih</dt><dd>{html.escape(completed)}</dd></div>")
    meta_html = f'<dl class="case-meta">{"".join(meta_bits)}</dl>' if meta_bits else ""

    about = block("Proje hakkında", p(html.escape(description))) if description else block(
        "Proje kaydı",
        p(
            f"{html.escape(name)} için Malt Studio uygulama kaydı.",
            (f"Konum: {html.escape(location)}." if location else ""),
            (f"Kategori: {html.escape(category)}." if category else ""),
            "Sayfadaki fotoğraflar bu işe aittir.",
            "Ölçü, malzeme ve montaj notları teklif dosyasındadır; burada uydurma metrik yazılmaz.",
        ),
    )

    applied = ""
    if labels:
        lis = []
        for label, s in resolved:
            text = html.escape(ALL_SERVICES[s] if s else label)
            if s:
                lis.append(f'<li><a href="/hizmetler/{s}/">{text}</a></li>')
            else:
                lis.append(f"<li>{text}</li>")
        applied = block("Uygulanan hizmet", f'<ul class="scope-list">{"".join(lis)}</ul>')

    photo_html = ""
    if images:
        figs = []
        for i, src in enumerate(images):
            figs.append(_picture(src, f"{name} uygulama projesi", lazy=i > 0))
        photo_html = (
            '<div class="content-block"><h2>Proje fotoğrafları</h2>'
            + "".join(figs)
            + "</div>"
        )

    svc_cards = cards(
        [
            (f"/hizmetler/{s}/", ALL_SERVICES[s], f"{ALL_SERVICES[s]} hizmeti.", "Hizmet")
            for _, s in known
        ]
    )
    svc_section = ""
    if svc_cards:
        svc_section = f"""<section class="section-band paper-band" aria-labelledby="rel-svc">
  <div class="wrap">
    <h2 id="rel-svc">İlgili hizmet</h2>
    <div class="card-grid">{svc_cards}</div>
  </div>
</section>"""

    others = [
        p for p in load_portfolio() if str(p.get("slug") or "").strip().strip("/") != slug
    ]
    rel_cards = cards(
        [
            (
                f"/projeler/{html.escape(str(p['slug']).strip().strip('/'))}/",
                html.escape(str(p["name"]).strip()),
                "Uygulama projesi.",
                "Proje",
            )
            for p in others
        ]
    )
    rel_section = ""
    if rel_cards:
        rel_section = f"""<section class="section-band" aria-labelledby="rel-prj">
  <div class="wrap">
    <h2 id="rel-prj">Diğer projeler</h2>
    <div class="card-grid">{rel_cards}</div>
  </div>
</section>"""

    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        breadcrumb_ld(
            [
                ("Ana Sayfa", f"{SITE}/"),
                ("Projeler", f"{SITE}/projeler/"),
                (name, canonical),
            ]
        ),
    )

    page = f"""{head(html.escape(title), html.escape(desc), canonical, json_ld=json_ld)}
<body>
{header()}
<article class="case-study">
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Projeler","/projeler/"),(safe_name,None))}
    <div class="eyebrow">Proje</div>
    <h1>{safe_name}</h1>
    <p class="lede">{html.escape(desc)}</p>
    {meta_html}
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa(f"Merhaba, {name} benzeri bir proje için teklif almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {about}
    {applied}
    {photo_html}
  </div>
</section>
{svc_section}
{rel_section}
{related_rail(hubs=[
    ("/projeler/", "Projeler", "Tamamladığımız işlerden örnekler."),
    ("/hizmetler/", "Hizmetler", "Tüm hizmetlerimize göz atın."),
    ("/bolgeler/tekirdag/", "Tekirdağ", "Tekirdağ yerel hizmet rehberi."),
    ("/", "Ana sayfa", "Malt Studio ana sayfa."),
])}
{cta_band("Benzer bir iş için yazın", f"{name} benzeri proje")}
</article>
{footer()}
</body></html>
"""
    write(ROOT / "projeler" / slug / "index.html", page)


def build_projeler_hub() -> None:
    items = load_portfolio()
    project_cards = cards(
        [
            (
                f"/projeler/{html.escape(str(p['slug']).strip().strip('/'))}/",
                html.escape(str(p["name"]).strip()),
                "Uygulama projesi.",
                "Proje",
            )
            for p in items
        ]
    )
    listing = (
        f'<section class="section-band paper-band"><div class="wrap">'
        f'<h2>Seçili işler</h2>'
        f'<div class="card-grid">{project_cards}</div></div></section>'
        if project_cards
        else ""
    )
    canonical = f"{SITE}/projeler/"
    title = "Projeler | Malt Studio İş Örnekleri"
    desc = "Tabela, ışıklı tabela, kutu harf ve giydirme proje örnekleri."
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        breadcrumb_ld([("Ana Sayfa", "/"), ("Projeler", canonical)]),
    )
    html_doc = f"""{head(title, desc, canonical, json_ld=json_ld)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa","/"),("Projeler",None))}
    <h1>Projeler</h1>
    <p class="lede">Tamamladığımız işlerden örnekler.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="{wa("Yeni proje")}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
    </div>
  </div>
</section>
{listing}
<section class="page-main">
  <div class="wrap">
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
    write(ROOT / "projeler" / "index.html", html_doc)


INDUSTRY_COPY = {
    "fabrika-osb": (
        "Sanayi tesislerinde tabela; kimlik, yön ve dayanımdır.",
        ["Tesis totemi", "Cephe yazısı", "İSG levhaları", "Filo giydirme", "Saha yön tabelaları"],
        ["totem", "tabela", "kutu-harf", "arac-giydirme", "is-guvenligi-tabelalari"],
        [],
    ),
    "restoran-cafe": (
        "F&B’de tabela ve vitrin ilk karar anını yönetir.",
        ["Işıklı cephe", "Vitrin giydirme", "Gece okunurluk", "Kampanya yüzeyleri"],
        ["isikli-tabela", "cam-giydirme", "tabela", "lightbox"],
        ["kosem-doner", "pembe-pasta-evi"],
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
        ["ofiso", "okka-tarim"],
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
        ["pembe-pasta-evi", "kosem-doner"],
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
    bil_links = [(h, article_title(h), "Karar rehberi.") for h in a5["knowledge"]]
    canonical = f"{SITE}/sektorler/{slug}/"
    title = f"{name} Tabela ve Görünürlük Çözümleri"
    desc = f"{name} sektörü için tabela ve görünürlük. Malt Studio."
    faqs = [
        (
            f"{name} için hangi hizmetler?",
            ", ".join(
                f'<a href="/hizmetler/{s}/">{ALL_SERVICES[s]}</a>'
                for s in services
                if s in ALL_SERVICES
            )
            + ".",
        ),
        ("Bu hizmet sayfasının yerine geçer mi?", "Hayır; sektör sayfası dikey girişidir. Üretim ilgili hizmet URL’sindedir."),
        ("Tekirdağ’da uygulanır mı?", 'Evet; keşif <a href="/bolgeler/tekirdag/">Tekirdağ atölyesinden</a> planlanır.'),
        ("Teklif nasıl alınır?", "WhatsApp veya telefon ile keşif talebi bırakın. Sabit internet fiyatı yoktur."),
    ]
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        breadcrumb_ld([("Ana Sayfa", "/"), ("Sektörler", "/sektorler/"), (name, canonical)]),
        faq_ld(canonical, faqs),
    )
    html = f"""{head(title, desc, canonical, json_ld=json_ld)}
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
    {mid_cta(f"{name} sektörü keşif")}
  </div>
</section>
{related_rail(services=svc_links, knowledge=bil_links)}
<section class="section-band paper-band">
    <div class="wrap"><h2>SSS</h2><div class="faq">{faq_html(faqs)}</div></div>
</section>
{cta_band(f"{name} için keşif", f"{name} keşif")}
{footer()}
</body></html>
"""
    write(ROOT / "sektorler" / slug / "index.html", html)


def build_sektorler_hub() -> None:
    items = cards([(f"/sektorler/{s}/", n, f"{n} çözümleri.", "Sektör") for s, n, pk in INDUSTRIES])
    canonical = f"{SITE}/sektorler/"
    title = "Sektörler | Fabrika, Restoran, Sağlık, Plaza"
    desc = "Sektörel tabela ve görünürlük çözümleri."
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        breadcrumb_ld([("Ana Sayfa", "/"), ("Sektörler", canonical)]),
    )
    html = f"""{head(title, desc, canonical, json_ld=json_ld)}
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
<section class="page-main"><div class="wrap">{block("Nasıl kullanılır?", p("Sektörünüzü seçin, ilgili hizmetlere ve projelere geçin.",'Kararsızsanız <a href="/bolgeler/tekirdag/">Tekirdağ atölye</a> sayfasına veya WhatsApp ile yazın.'))}{mid_cta("Sektör keşfi")}</div></section>
<section class="section-band paper-band"><div class="wrap"><div class="card-grid">{items}</div></div></section>
{related_rail(
    services=[(f"/hizmetler/{s}/", n, "Hizmet.") for s, n in list(A0.items())[:6]],
    knowledge=[(f"/bilgi/{s}/", t, "Rehber.") for s, t, _, _ in ARTICLES[:3]],
    projects=["ofiso", "kosem-doner", "pembe-pasta-evi"],
)}
{cta_band("Sektörünüze uygun çözüm", "Sektör keşfi")}
{footer()}
</body></html>
"""
    write(ROOT / "sektorler" / "index.html", html)


ARTICLE_BODY = {
    "tabela-cesitleri": [
        (
            "Giriş",
            "Tabela seçimi estetik bir katalog işareti değildir. Okunurluk, dayanım, montaj yüzeyi, rüzgâr/yükseklik ve gece ihtiyacı birlikte bakılır. Gündüz yeten ışıksız tabela, gece açık bir işletmede kaybolur; LED’li sistem ise elektrik ve servis katmanı ister. Kutu harf üç boyutlu cephe yazısıdır. Totem yol ve tesis yaklaşımını taşır; taşınabilir indoor display ayrı ailedir. Cam giydirme vitrin mesajı ile gizliliği dengeler. Lightbox perakende içi ışıklı kutu ve çerçevedir; cephe ışıklı tabela ile karıştırılmamalıdır. Aşağıdaki tablo türleri ayırır. Üretim, keşif ve yazılı teklif "
            '<a href="/hizmetler/tabela/">tabela üretimi</a> sayfasındadır. Sabit internet fiyatı yoktur. Tekirdağ Süleymanpaşa atölyesinden keşif planlanır; adres ve saat '
            '<a href="/bolgeler/tekirdag/">atölye sayfasındadır</a>.',
        ),
        ("Işıksız tabela", "Gündüz odaklı, genelde daha ekonomik cephe çözümleridir. Gece ihtiyacı yoksa doğru tercihtir."),
        ("Işıklı tabela", 'Gece görünürlük gereken noktalarda LED’li sistemler kullanılır. Ayrı hizmet: <a href="/hizmetler/isikli-tabela/">ışıklı tabela</a>.'),
        ("Kutu harf", 'Üç boyutlu cephe yazısıdır; prestij ve derinlik sağlar. Ayrı hizmet: <a href="/hizmetler/kutu-harf/">kutu harf</a>.'),
        ("Totem", 'Yol ve tesis yaklaşımında uzaktan algı için dikey sistemlerdir. Ayrı hizmet: <a href="/hizmetler/totem/">totem</a>.'),
        ("Cam giydirme", 'Vitrin mesajı ve gizlilik/görünürlük dengesi için folyo uygulamalarıdır. Ayrı hizmet: <a href="/hizmetler/cam-giydirme/">cam giydirme</a>.'),
        ("Lightbox", 'İç mekân/retail ışıklı kutu sistemidir; ışıklı tabela ile karıştırılmamalıdır. Ayrı hizmet: <a href="/hizmetler/lightbox/">lightbox</a>.'),
        ("Seçim çerçevesi", "Konum, gece ihtiyacı, bütçe, izin ve montaj yüzeyi birlikte değerlendirilir."),
    ],
    "isikli-mi-isiksiz-mi": [
        (
            "Karar sorusu",
            "İşletmeniz gece de görünmek zorunda mı? Bu soru çoğu tercihi belirler. Gece kapalı bir noktada LED, kasa ve güç kaynağı yatırımı çoğu zaman gereksizdir. Gece açık mağaza, eczane veya plaza girişinde ışıksız tabela kaybolur. Işıklı sistem elektrik hattı, kasa derinliği ve servis erişimi ister; ışıksız sistemde bu katman yoktur. Lightbox ayrı üründür: perakende içi ışıklı kutu veya çerçeve, cephe LED tabela değildir. Neon şart değildir; LED ışıklı tabela yaygındır. Aşağıdaki tablo farkı özetler. Karar sonrası üretim "
            '<a href="/hizmetler/isikli-tabela/">ışıklı tabela</a> veya '
            '<a href="/hizmetler/tabela/">tabela</a> sayfasından yürür. Net rakam keşif sonrası yazılı verilir; sabit liste yoktur.',
        ),
        ("Görünürlük", "Işıklı gece avantajı sağlar; ışıksız gündüz yeterli olabilir."),
        ("Maliyet", "Işıklıda kasa, LED ve elektrik maliyeti eklenir. Sabit m² fiyatı yayınlanmaz."),
        ("Bakım", "LED ve güç kaynakları servis gerektirebilir."),
        ("Cephe ve izin", "Mimari ve elektrik altyapısı seçimi etkiler."),
        ("Lightbox ayrımı", 'Lightbox ayrı üründür; cephe ışıklı tabela değildir. Ayrı hizmet: <a href="/hizmetler/lightbox/">lightbox</a>.'),
        ("Sonuç", 'Ticari uygulama için <a href="/hizmetler/isikli-tabela/">ışıklı tabela</a> veya <a href="/hizmetler/tabela/">tabela</a> sayfasına geçin.'),
    ],
    "kutu-harf-malzemeler": [
        (
            "Amaç",
            "Malzeme karşılaştırması bilgilendirmedir; tek kazanan ilan edilmez. Pleksi (akrilik) ışıklı harfte renk ve ışık geçirgenliği için yaygındır. Paslanmaz dış dayanım ve prestij algısı için seçilir; bütçe genelde daha yüksektir. Işıklı/ışıksız tercih çoğu zaman malzemeden önce netleşir. Montaj yüzeyi — kompozit, beton, cam — aparat tipini belirler; keşifsiz sipariş risklidir. Channel letters kutu harfin uluslararası adıdır; ayrı doorway URL yoktur. Üretim ve teklif "
            '<a href="/hizmetler/kutu-harf/">kutu harf</a> sayfasındadır. Vektörel logo kaliteyi yükseltir; yoksa sade alternatif konuşulur.',
        ),
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
        ("Ticari sayfa", 'Uygulama <a href="/hizmetler/cam-giydirme/">cam giydirme</a> altındadır.'),
    ],
    "arac-giydirme-rehberi": [
        ("Süreç", "Ölçü → tasarım → baskı → yüzey hazırlığı → uygulama."),
        ("Full vs parça", "Bütçe ve marka alanına göre seçilir."),
        ("Filo", "Şablon standardı + araç tipi uyarlaması."),
        ("Ömür", "Folyo tipi, yıkama, güneş ve kullanım."),
        ("Söküm", "Doğru folyo ile kontrollü söküm hedeflenir."),
        ("Ticari sayfa", '<a href="/hizmetler/arac-giydirme/">Araç giydirme</a> hizmet sayfasından teklif alınır.'),
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
        ("Indoor display", 'Display/POS sayfasına aittir: <a href="/hizmetler/display-pos/">Display & POS</a>.'),
        ("Ticari sayfa", '<a href="/hizmetler/totem/">Totem</a> hizmet sayfası.'),
    ],
}


def build_article(slug: str, title: str, primary: str, pk: str) -> None:
    sections = ARTICLE_BODY[slug]
    a5 = ARTICLE_A5[slug]
    body: list[str] = []
    for i, (h, para) in enumerate(sections):
        body.append(block(h, p(para)))
        if i == 0 and slug in ARTICLE_TABLES:
            heading, headers, rows = ARTICLE_TABLES[slug]
            body.append(block(heading, table(headers, rows)))
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
    projs = SERVICE_DEPTH.get(primary, {}).get("related_projects", [])
    other_bilgi = [
        (f"/bilgi/{s}/", t, "İlgili rehber.")
        for s, t, _, _ in ARTICLES
        if s != slug
    ][:3]
    svc_name = ALL_SERVICES.get(primary, primary)
    faqs = a5["faqs"] + [
        ("İlgili hizmet nerede?", f'Üretim ve teklif <a href="/hizmetler/{primary}/">{svc_name}</a> sayfasındadır.'),
        ("Daha fazla rehber?", '<a href="/bilgi/">Bilgi merkezi</a> diğer karşılaştırmaları listeler.'),
    ]
    role_link = (
        f'Üretim ve teklif için <a href="/hizmetler/{primary}/">{svc_name}</a> '
        "sayfasına bakabilirsiniz."
    )
    wa_msg = f"{svc_name} hakkında bilgi"
    canonical = f"{SITE}/bilgi/{slug}/"
    desc = f"{title} — eğitici rehber. Malt Studio bilgi merkezi."
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        article_ld(canonical, title, desc),
        breadcrumb_ld([("Ana Sayfa", "/"), ("Bilgi", "/bilgi/"), (title, canonical)]),
        faq_ld(canonical, faqs),
    )
    html = f"""{head(title, desc, canonical, json_ld=json_ld)}
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
    canonical = f"{SITE}/bilgi/"
    title = "Bilgi Merkezi | Tabela ve Reklam Rehberleri"
    desc = "Tabela çeşitleri, karşılaştırmalar ve uygulama rehberleri."
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        breadcrumb_ld([("Ana Sayfa", "/"), ("Bilgi", canonical)]),
    )
    html = f"""{head(title, desc, canonical, json_ld=json_ld)}
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
<section class="page-main"><div class="wrap">{block("Nasıl okumalı?", p("Önce ihtiyacınızı seçin, sonra ilgili hizmete geçin.","Fiyat eğitimi teklif yerine geçmez."))}{mid_cta("Bilgi sonrası teklif")}</div></section>
<section class="section-band paper-band"><div class="wrap"><div class="card-grid">{items}</div></div></section>
{related_rail(
    services=[(f"/hizmetler/{s}/", n, f"{n} hizmeti.") for s, n in list(A0.items())[:6]],
    projects=["ofiso", "kosem-doner", "anka"],
    industries=[(f"/sektorler/{s}/", n, f"{n} çözümleri.") for s, n, _ in INDUSTRIES[:4]],
)}
{cta_band("Rehberden uygulamaya geçin", "Bilgi sonrası teklif")}
{footer()}
</body></html>
"""
    write(ROOT / "bilgi" / "index.html", html)


def _html_for_url(url: str) -> Path:
    path = url[len(SITE) :] if url.startswith(SITE) else url
    if path in ("", "/"):
        return ROOT / "index.html"
    return ROOT / path.strip("/") / "index.html"


def _lastmod(path: Path) -> str | None:
    if not path.is_file():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")


def build_gizlilik() -> None:
    """Short privacy notice from actual site practices. Not a fabricated KVKK registration."""
    canonical = f"{SITE}/gizlilik/"
    title = "Gizlilik ve Kişisel Veriler | Malt Studio"
    desc = "Malt Studio sitesinde iletişim ve analitik kullanımı hakkında kısa bilgilendirme."
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        breadcrumb_ld([("Ana Sayfa", "/"), ("Gizlilik", canonical)]),
    )
    html = f"""{head(title, desc, canonical, json_ld=json_ld)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Gizlilik", None))}
    <h1>Gizlilik</h1>
    <p class="lede">Sitede hangi bilgilerin işlendiğine dair kısa not. Bu metin avukat onaylı tam KVKK politikası değildir.</p>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Veri sorumlusu", p(
        "Malt Studio, Tekirdağ Süleymanpaşa.",
        f"Adres: {ADDRESS_ONE_LINE}.",
        f'E-posta: <a href="mailto:{EMAIL}">{EMAIL}</a>. Telefon: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.',
    ))}
    {block("İletişim kanalları", p(
        "WhatsApp, telefon ve e-posta ile gönderdiğiniz keşif/teklif mesajları işin planlanması için kullanılır.",
        "Mesaj içeriği üçüncü kişilere satılmaz.",
    ))}
    {block("Analitik", p(
        "Sitede Google Analytics 4 (ölçüm kimliği content.json içinde tanımlıysa) sayfa görüntüleme istatistiği için kullanılır.",
        "Reklam kişiselleştirme veya uydurma kullanıcı profilleri bu sayfada iddia edilmez.",
    ))}
    {block("Haklar", p(
        "Kişisel verilerinizle ilgili talep için e-posta veya telefon kullanın.",
        'Atölye ve iletişim: <a href="/bolgeler/tekirdag/">Tekirdağ atölye sayfası</a>.',
    ))}
  </div>
</section>
{cta_band("Keşif için yazın", "Keşif talebi")}
{footer()}
</body></html>
"""
    write(ROOT / "gizlilik" / "index.html", html)


def build_hakkimizda() -> None:
    """About page from existing CMS/footer copy only. No invented founder or metrics."""
    canonical = f"{SITE}/hakkimizda/"
    title = "Hakkımızda | Malt Studio"
    desc = "Tekirdağ merkezli reklam ve tabela üreticisi. Üretim, montaj ve keşif."
    json_ld = page_graph(
        webpage_ld(canonical, title, desc),
        website_node(),
        breadcrumb_ld([("Ana Sayfa", "/"), ("Hakkımızda", canonical)]),
    )
    html = f"""{head(title, desc, canonical, json_ld=json_ld)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Ana Sayfa", "/"), ("Hakkımızda", None))}
    <h1>Hakkımızda</h1>
    <p class="lede">Tekirdağ Süleymanpaşa merkezli reklam ve tabela üretimi.</p>
  </div>
</section>
<section class="page-main">
  <div class="wrap">
    {block("Ne yapıyoruz", p(
        "Malt Studio Tekirdağ merkezli reklam ajansı ve tabela üreticisidir. Tabela, kurumsal kimlik, dijital baskı ve uygulama — keşiften montaja.",
        "Şube sayısı, uydurma sertifika veya sahte yorum eklenmez.",
    ))}
    {block("Nerede", p(
        f"{ADDRESS_ONE_LINE}.",
        f"Çalışma saatleri: {HOURS_DISPLAY}.",
        f'İletişim: <a href="/bolgeler/tekirdag/">atölye sayfası</a>.',
        f'Telefon: <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>.',
    ))}
    {block("Hizmetler", p(
        'Tüm hizmet listesi <a href="/hizmetler/">hizmetler</a> sayfasındadır. Seçili işler <a href="/projeler/">projeler</a> altındadır.',
    ))}
  </div>
</section>
{cta_band("Keşif için yazın", "Keşif talebi")}
{footer()}
</body></html>
"""
    write(ROOT / "hakkimizda" / "index.html", html)


def write_404() -> None:
    html = f"""{head("Sayfa bulunamadı | Malt Studio", "İstediğiniz sayfa yok. Hizmetler, projeler veya atölye sayfasına gidin.", f"{SITE}/404.html", noindex=True)}
<body>
{header()}
<section class="page-hero">
  <div class="wrap">
    <h1>Sayfa bulunamadı</h1>
    <p class="lede">Bu adres yayında değil. Aşağıdan devam edin.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="/">Ana sayfa</a>
      <a class="btn btn-ghost" href="/hizmetler/">Hizmetler</a>
      <a class="btn btn-ghost" href="/bolgeler/tekirdag/">Tekirdağ atölye</a>
    </div>
  </div>
</section>
{footer()}
</body></html>
"""
    write(ROOT / "404.html", html)


def merge_sitemap() -> None:
    """Indexable public URLs. lastmod from the HTML file mtime after this write pass."""
    urls = [
        f"{SITE}/",
        f"{SITE}/hizmetler/",
        f"{SITE}/bolgeler/tekirdag/",
        f"{SITE}/projeler/",
        f"{SITE}/sektorler/",
        f"{SITE}/bilgi/",
        f"{SITE}/gizlilik/",
        f"{SITE}/hakkimizda/",
    ]
    for s in ALL_SERVICES:
        urls.append(f"{SITE}/hizmetler/{s}/")
    for item in load_portfolio():
        urls.append(f"{SITE}/projeler/{str(item['slug']).strip().strip('/')}/")
    for slug, *_ in INDUSTRIES:
        urls.append(f"{SITE}/sektorler/{slug}/")
    for slug, *_ in ARTICLES:
        urls.append(f"{SITE}/bilgi/{slug}/")
    parts = []
    for u in urls:
        lm = _lastmod(_html_for_url(u))
        if lm:
            parts.append(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{lm}</lastmod>\n  </url>")
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
    for item in load_portfolio():
        build_project(item)
    build_sektorler_hub()
    for slug, name, pk in INDUSTRIES:
        build_industry(slug, name, pk)
    build_bilgi_hub()
    for slug, title, primary, pk in ARTICLES:
        build_article(slug, title, primary, pk)
    build_gizlilik()
    build_hakkimizda()
    write_404()
    # Wave A3 homepage authority (no new URLs)
    import importlib.util

    a3_path = ROOT / "scripts" / "build_home_a3.py"
    spec = importlib.util.spec_from_file_location("build_home_a3", a3_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    mod.main()
    merge_sitemap()
    print("Production upgrade complete.")


if __name__ == "__main__":
    main()
