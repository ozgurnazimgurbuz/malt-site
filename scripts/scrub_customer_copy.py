#!/usr/bin/env python3
"""Remove internal SEO strategy jargon from published customer-facing HTML."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN = re.compile(
    r"S×C|money keyword|money H1|Money H1|Geo-money|geo-money|geo niyet|Geo niyet|"
    r"geo fiyat|Geo fiyat|Ownership:|owner URL|Wave A2|city hub|City hub|"
    r"Service × City|Non-geo|geo-money H1|Owner PK|owner PK|"
    r"Anti-doorway|doorway|cannibalization|money PK|Service×City",
    re.I,
)

# Title → short customer blurb for related cards
BLURB_BY_TITLE = {
    "Tabela Fiyatını Neler Etkiler?": "Fiyatı etkileyen faktörler.",
    "Tabela Çeşitleri": "Hangi tabela tipi ne zaman seçilir.",
    "Işıklı mı Işıksız mı?": "Gece görünürlük karar rehberi.",
    "Kutu Harf Malzemeler": "Pleksi, paslanmaz ve seçim kriterleri.",
    "One Way Vision Nedir?": "Vitrin folyo mantığı.",
    "Araç Giydirme Rehberi": "Kaplama öncesi bilmeniz gerekenler.",
    "Totem Seçim Rehberi": "Yol ve giriş totem kararları.",
    "Tekirdağ Tabela": "Tekirdağ’da tabela üretimi ve montajı.",
    "Tekirdağ Işıklı Tabela": "Tekirdağ’da ışıklı tabela hizmeti.",
    "Tekirdağ Işıklı": "Tekirdağ’da ışıklı tabela hizmeti.",
    "Tekirdağ Kutu Harf": "Tekirdağ’da kutu harf üretimi.",
    "Tekirdağ Totem": "Tekirdağ’da totem tabela uygulamaları.",
    "Tekirdağ Araç Giydirme": "Tekirdağ’da araç giydirme hizmeti.",
    "Tekirdağ Araç": "Tekirdağ’da araç giydirme hizmeti.",
    "Tekirdağ Cam Giydirme": "Tekirdağ’da cam giydirme uygulamaları.",
    "Tekirdağ Cam": "Tekirdağ’da cam giydirme uygulamaları.",
    "Tabela": "Tabela üretimi ve montajı.",
    "Işıklı Tabela": "LED ışıklı tabela sistemleri.",
    "Kutu Harf": "Pleksi ve paslanmaz kutu harf.",
    "Totem": "Yol ve tesis totem sistemleri.",
    "Araç Giydirme": "Filo ve ticari araç kaplama.",
    "Cam Giydirme": "One way vision ve vitrin folyo.",
    "Lightbox": "Işıklı kutu ve SEG lightbox.",
    "Display & POS": "Mağaziçi display ve POS.",
    "Ofis Branding": "Ofis ve plaza iç kimlik.",
    "İş Güvenliği Tabelaları": "İş güvenliği ve uyarı tabelaları.",
    "Fabrikalar / OSB": "Tesis kimliği, totem ve iş güvenliği.",
    "Fabrika & OSB": "Tesis kimliği, totem ve iş güvenliği.",
    "Perakende": "Mağaza cephe ve vitrin çözümleri.",
    "Restoran / Cafe": "Tabela, cam ve menü yüzeyleri.",
    "Restoran & Cafe": "Tabela, cam ve menü yüzeyleri.",
    "Plaza / Ofis": "Ofis branding ve giriş kimliği.",
    "Plaza & Ofis": "Ofis branding ve giriş kimliği.",
    "İnşaat / Şantiye": "Geçici ve kalıcı saha işaretleri.",
    "İnşaat & Şantiye": "Geçici ve kalıcı saha işaretleri.",
    "Sağlık": "Klinik ve sağlık noktası görünürlüğü.",
    "Liman Kahve": "Mağaza tabela ve cephe görünürlüğü.",
    "Volt Enerji": "Tesis kimliği ve yönlendirme.",
    "Kuzey Tekstil": "OSB tesis tabela uygulamaları.",
    "Mera Otel": "Konaklama giriş ve cephe kimliği.",
    "Dörtnal": "Perakende vitrin ve tabela.",
    "Ekip Yazılım": "Ofis branding ve giriş kimliği.",
    "Hizmetler": "Tüm hizmetlerimize göz atın.",
    "Bilgi": "Rehberler ve karar içerikleri.",
    "Projeler": "Tamamladığımız işlerden örnekler.",
    "Sektörler": "Sektöre özel çözümler.",
    "Tekirdağ": "Tekirdağ yerel hizmet rehberi.",
    "Ana sayfa": "Malt Studio ana sayfa.",
    "Rehber": "Karar vermenize yardımcı rehber.",
}


def blurb_for(title: str) -> str:
    t = re.sub(r"\s+", " ", title).strip()
    if t in BLURB_BY_TITLE:
        return BLURB_BY_TITLE[t]
    if t.startswith("Tekirdağ "):
        rest = t[len("Tekirdağ ") :].strip()
        return f"Tekirdağ’da {rest.lower()} hizmeti."
    return "İlgili sayfa."


BAD_CARD_P = re.compile(
    r"(?:İlgili rehber — money H1 taşımaz\.|"
    r"Eğitim — money H1 değil\.|"
    r"Dikey giriş — money H1 değil\.|"
    r"Dikey giriş money H1 taşımaz\.|"
    r"Geo-money owner\.?|"
    r"Geo-money\.?|"
    r"İlgili yerel sayfa\.|"
    r"Non-geo parent owner\.|"
    r"Non-geo hizmet\.|"
    r"Yerel ticari owner\.|"
    r"Örnek geo-money sayfa\.|"
    r"Geo-money owner sayfa\.|"
    r"Hizmet owner\.|"
    r"Ticari owner\.|"
    r"Önerilen hizmet owner\.|"
    r"Vaka / kanıt düğümü\.|"
    r"İlgili vaka — kanıt kapısı açık\.|"
    r"İlgili hizmet — ayrı PK\.|"
    r"İlgili hizmet\.|"
    r"Eğitim\.|"
    r"Dikey\.|"
    r"Yerel firma / city hub\.|"
    r"Hizmet hub|"
    r"Rehber hub|"
    r"Kanıt hub|"
    r"Dikey hub|"
    r"City hub|"
    r"Authority hub|"
    r"PK: [^<]+)",
    re.I,
)


def scrub_card_blocks(html: str) -> str:
    def repl(m: re.Match) -> str:
        open_tag, h3, p_open, p_body, p_close, rest = (
            m.group(1),
            m.group(2),
            m.group(3),
            m.group(4),
            m.group(5),
            m.group(6),
        )
        title = re.sub(r"<[^>]+>", "", h3).strip()
        body = p_body.strip()
        if BAD_CARD_P.fullmatch(body) or FORBIDDEN.search(body):
            body = blurb_for(title)
        # meta S×C → Yerel
        rest = re.sub(
            r'(<span class="meta">)S×C(</span>)',
            r"\1Yerel\2",
            rest,
        )
        return f"{open_tag}<h3>{h3}</h3>{p_open}{body}{p_close}{rest}"

    # local-card / card / knowledge-card patterns with h3 + p
    return re.sub(
        r'(<a class="(?:local-card|card|knowledge-card)"[^>]*>)\s*'
        r"<h3>(.*?)</h3>\s*"
        r"(<p[^>]*>)(.*?)(</p>)"
        r"(.*?</a>)",
        repl,
        html,
        flags=re.S | re.I,
    )


SENTENCE_KILL = re.compile(
    r"(?<=[.!?…])\s*"
    r"[^.!?…]*?"
    r"(?:S×C|money H1|Money H1|Geo-money|geo-money|geo niyet|Geo niyet|"
    r"geo fiyat|Geo fiyat|Ownership:|owner URL|Wave A2|city hub|City hub|"
    r"Service × City|Non-geo|owner PK|Owner PK|Anti-doorway|"
    r"money keyword|money PK|Service×City|geo-money H1|doorway|"
    r"Yerel niyet Tekirdağ|Tekirdağ özelinde geo|Tekirdağ niyeti S×C|"
    r"Tekirdağ filo niyeti|Yerel Tekirdağ niyeti|ayrı S×C|"
    r"Ayrı S×C|bu S×C|ilgili S×C|S×C sayfa|S×C URL|"
    r"S×C’|S×C')"
    r"[^.!?…]*[.!?…]?",
    re.I,
)

# Also kill sentences that start a paragraph with jargon
LEAD_KILL = re.compile(
    r"(<(?:p|li)[^>]*>)\s*"
    r"([^<]*?(?:S×C|money H1|Money H1|Geo-money|geo niyet|Ownership:|"
    r"owner URL|Wave A2|city hub|Service × City|Anti-doorway|"
    r"money keyword|Non-geo parent|Owner PK)[^<]*?)(</(?:p|li)>)",
    re.I,
)


def scrub_sentences(html: str) -> str:
    # Remove ownership note paragraphs entirely
    html = re.sub(
        r'\s*<p class="note">Ownership:[\s\S]*?</p>',
        "",
        html,
        flags=re.I,
    )
    # Remove standalone jargon-only paragraphs
    html = re.sub(
        r"\s*<p>(?:Wave A2’de ayrı S×C yok[^<]*|Ayrı S×C URL’si yoktur[^<]*|"
        r"Ayrı S×C yok[^<]*|Bu sayfa coğrafyasız[^<]*S×C[^<]*|"
        r"Yerel niyet için Tekirdağ[^<]*S×C[^<]*|"
        r"Tekirdağ plaza işlerinde S×C[^<]*|"
        r"Tekirdağ filo işleri S×C[^<]*|"
        r"Geo niyet için ilgili S×C[^<]*|"
        r"“Tekirdağ [^”]+” geo-money[^<]*|"
        r"Bu sayfa coğrafyasız ticari niyeti taşır[^<]*|"
        r"Bu hizmet için ayrı Service×City[^<]*|"
        r"Anti-doorway:[^<]*|"
        r"Süleymanpaşa / merkez talepleri bu URL ve Tekirdağ city hub[^<]*|"
        r"Owner PK:[^<]*|"
        r"Bu sayfa dikey giriştir; bare service money PK[^<]*|"
        r"Aşağıdaki hizmetler bu dikeyde sık bir araya gelir\. Her biri kendi owner URL’sine sahiptir\.</p>)",
        "",
        html,
        flags=re.I,
    )

    def kill_lead(m: re.Match) -> str:
        open_t, text, close_t = m.group(1), m.group(2), m.group(3)
        if FORBIDDEN.search(text) and len(text) < 220:
            # whole short paragraph is jargon — drop content
            return f"{open_t}{close_t}"
        cleaned = SENTENCE_KILL.sub("", text)
        cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
        if not cleaned or FORBIDDEN.search(cleaned):
            # strip remaining forbidden clauses clumsily
            cleaned = FORBIDDEN.sub("", cleaned)
            cleaned = re.sub(r"\s{2,}", " ", cleaned).strip(" .;")
        if not cleaned:
            return f"{open_t}{close_t}"
        return f"{open_t}{cleaned}{close_t}"

    html = LEAD_KILL.sub(kill_lead, html)

    # Sentence-level removal inside longer tags
    def scrub_text_nodes(m: re.Match) -> str:
        tag_open, text, tag_close = m.group(1), m.group(2), m.group(3)
        if not FORBIDDEN.search(text):
            return m.group(0)
        cleaned = SENTENCE_KILL.sub("", text)
        # leftover fragments that still contain terms
        if FORBIDDEN.search(cleaned):
            parts = re.split(r"(?<=[.!?…])\s+", cleaned)
            parts = [p for p in parts if p and not FORBIDDEN.search(p)]
            cleaned = " ".join(parts)
        cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
        if not cleaned:
            return f"{tag_open}{tag_close}"
        return f"{tag_open}{cleaned}{tag_close}"

    html = re.sub(
        r"(<(?:p|li|div class=\"eyebrow\"|span class=\"meta\")[^>]*>)([^<]+)(</(?:p|li|div|span)>)",
        scrub_text_nodes,
        html,
        flags=re.I,
    )
    return html


def scrub_eyebrows_and_meta(html: str) -> str:
    html = re.sub(
        r'<div class="eyebrow">Service × City · Geo-money owner</div>',
        '<div class="eyebrow">Tekirdağ’da Hizmet</div>',
        html,
    )
    html = re.sub(
        r'<div class="eyebrow">City hub · Local / firm owner</div>',
        '<div class="eyebrow">Tekirdağ Yerel Rehber</div>',
        html,
    )
    html = re.sub(
        r'<div class="eyebrow">Hizmet · Owner PK: [^<]+</div>',
        '<div class="eyebrow">Hizmet</div>',
        html,
    )
    html = re.sub(
        r'<div class="eyebrow">Industry · PK: [^<]+</div>',
        '<div class="eyebrow">Sektör</div>',
        html,
    )
    html = re.sub(
        r'<div class="eyebrow">Knowledge · PK: [^<]+</div>',
        '<div class="eyebrow">Rehber</div>',
        html,
    )
    html = re.sub(
        r'<div class="eyebrow">Case study · EEAT proof node</div>',
        '<div class="eyebrow">Proje</div>',
        html,
    )
    html = re.sub(
        r'(<span class="meta">)S×C(</span>)',
        r"\1Yerel\2",
        html,
    )
    html = re.sub(
        r'<a class="chip is-alias" href="/bolgeler/tekirdag/">Süleymanpaşa \(alias\)</a>',
        '<a class="chip" href="/bolgeler/tekirdag/">Süleymanpaşa</a>',
        html,
    )
    return html


HOME_REPLACES = [
    (
        "Üretim ve uygulama kapasitemiz. Her kart mevcut hizmet sayfasına gider; yeni URL açılmaz. Geo niyetler S×C sayfalarındadır.",
        "Üretimden montaja, ihtiyacınıza uygun çözümler.",
    ),
    (
        "Tabela, ışıklı tabela, kutu harf ve uygulama — keşiften montaja.",
        "Üretimden montaja, ihtiyacınıza uygun çözümler.",
    ),
    (
        "Öne çıkan projeler. Detay sayfalarına geçin; görseller geldikçe güncellenir.",
        "Tamamladığımız işlerden öne çıkanlar.",
    ),
    (
        "Sektör sayfaları dikey bağlam taşır; money keyword sahipliği hizmet ve S×C URL’lerindedir.",
        "Farklı sektörlere özel çözümler sunuyoruz.",
    ),
    (
        "Fabrika, perakende, restoran, plaza ve şantiye için görünürlük çözümleri.",
        "Farklı sektörlere özel çözümler sunuyoruz.",
    ),
    (
        "Keşiften satış sonrasına kadar tek hat. Ayrı /surec/ URL’si yok; süreç buradadır.",
        "Keşiften teslimata kadar birlikte yürüdüğümüz süreç.",
    ),
    (
        "Eğitim ve karar rehberleri. Ticari money H1’ler hizmet sayfalarındadır.",
        "Karar vermenize yardımcı olacak rehberler.",
    ),
    (
        "Tekirdağ city hub yerel firma niyetini taşır. İlçe adları bilgilendirme amaçlıdır; yeni landing açılmaz. Süleymanpaşa alias’tır.",
        "Tekirdağ merkezliyiz; çevre ilçelere keşif ve montaj desteği sunuyoruz.",
    ),
]


def scrub_home_phrases(html: str) -> str:
    for old, new in HOME_REPLACES:
        html = html.replace(old, new)
    # local cards on home
    html = re.sub(
        r"(<a class=\"local-card\" href=\"/hizmet-bolge/tekirdag-tabela/\">\s*<h3>Tekirdağ Tabela</h3>\s*<p>)[^<]+(</p>)",
        r"\1Tekirdağ’da tabela üretimi ve montajı.\2",
        html,
    )
    html = re.sub(
        r"(<a class=\"local-card\" href=\"/hizmet-bolge/tekirdag-isikli-tabela/\">\s*<h3>Tekirdağ Işıklı</h3>\s*<p>)[^<]+(</p>)",
        r"\1Tekirdağ’da ışıklı tabela hizmeti.\2",
        html,
    )
    html = re.sub(
        r"(<a class=\"local-card\" href=\"/hizmet-bolge/tekirdag-kutu-harf/\">\s*<h3>Tekirdağ Kutu Harf</h3>\s*<p>)[^<]+(</p>)",
        r"\1Tekirdağ’da kutu harf üretimi.\2",
        html,
    )
    html = re.sub(
        r"(<a class=\"local-card\" href=\"/hizmet-bolge/tekirdag-totem/\">\s*<h3>Tekirdağ Totem</h3>\s*<p>)[^<]+(</p>)",
        r"\1Tekirdağ’da totem tabela uygulamaları.\2",
        html,
    )
    html = re.sub(
        r"(<a class=\"local-card\" href=\"/hizmet-bolge/tekirdag-arac-giydirme/\">\s*<h3>Tekirdağ Araç</h3>\s*<p>)[^<]+(</p>)",
        r"\1Tekirdağ’da araç giydirme hizmeti.\2",
        html,
    )
    html = re.sub(
        r"(<a class=\"local-card\" href=\"/hizmet-bolge/tekirdag-cam-giydirme/\">\s*<h3>Tekirdağ Cam</h3>\s*<p>)[^<]+(</p>)",
        r"\1Tekirdağ’da cam giydirme uygulamaları.\2",
        html,
    )
    return html


def scrub_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    html = original
    html = scrub_eyebrows_and_meta(html)
    html = scrub_home_phrases(html)
    html = scrub_card_blocks(html)
    html = scrub_sentences(html)
    # empty tags cleanup
    html = re.sub(r"<p>\s*</p>", "", html)
    html = re.sub(r"<li>\s*</li>", "", html)
    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def update_content_json() -> None:
    path = ROOT / "content.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["servicesIntro"] = "Üretimden montaja, ihtiyacınıza uygun çözümler."
    data["portfolioIntro"] = "Tamamladığımız işlerden öne çıkanlar."
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    update_content_json()
    changed = 0
    pages = [ROOT / "index.html"]
    for folder in (
        "hizmetler",
        "hizmet-bolge",
        "bolgeler",
        "projeler",
        "sektorler",
        "bilgi",
    ):
        pages.extend((ROOT / folder).rglob("index.html"))
    for path in sorted(set(pages)):
        if scrub_file(path):
            changed += 1
            print(f"scrubbed {path.relative_to(ROOT)}")
    print(f"done: {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
