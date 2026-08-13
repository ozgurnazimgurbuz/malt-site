#!/usr/bin/env python3
"""Shared shell, CTAs, EEAT blocks for production page builds."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://maltstudio.co"
PHONE_DISPLAY = "+90 552 582 69 59"
PHONE_TEL = "+905525826959"
WA = "905525826959"
EMAIL = "merhaba@maltstudio.co"
ADDRESS_STREET = "Yavuz Mahallesi, Ruşen Güneş Sokak, D Blok No:2"
ADDRESS_POSTAL = "59100"
ADDRESS_LOCALITY = "Süleymanpaşa"
ADDRESS_REGION = "Tekirdağ"
ADDRESS_COUNTRY = "Türkiye"
ADDRESS_ONE_LINE = (
    f"{ADDRESS_STREET}, {ADDRESS_POSTAL} {ADDRESS_LOCALITY} / {ADDRESS_REGION}, {ADDRESS_COUNTRY}"
)
HOURS_DISPLAY = "Pazartesi–Cumartesi 09:00–19:00"
_GA_ID_RE = re.compile(r"^G-[A-Z0-9]+$")


def google_analytics_id() -> str:
    """Read Measurement ID from content.json (empty if unset/invalid)."""
    path = ROOT / "content.json"
    if not path.exists():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    ga_id = (data.get("googleAnalyticsId") or "").strip()
    return ga_id if _GA_ID_RE.match(ga_id) else ""


def gtag_snippet(ga_id: str | None = None) -> str:
    """Deferred GA4 loader — idle/after-load so it stays off the LCP critical path."""
    ga_id = (ga_id or google_analytics_id()).strip()
    if not _GA_ID_RE.match(ga_id):
        return ""
    return (
        "<!-- Google tag (gtag.js) — deferred until idle -->\n"
        "<script>\n"
        "(function(){\n"
        f"  var id='{ga_id}';\n"
        "  window.dataLayer=window.dataLayer||[];\n"
        "  function gtag(){dataLayer.push(arguments);}\n"
        "  window.gtag=gtag;\n"
        "  function load(){\n"
        "    if(window.__gaLoaded)return;window.__gaLoaded=1;\n"
        "    var s=document.createElement('script');\n"
        "    s.async=true;\n"
        "    s.src='https://www.googletagmanager.com/gtag/js?id='+id;\n"
        "    s.onload=function(){gtag('js',new Date());gtag('config',id);};\n"
        "    document.head.appendChild(s);\n"
        "  }\n"
        "  if('requestIdleCallback' in window)requestIdleCallback(load,{timeout:4000});\n"
        "  else window.addEventListener('load',function(){setTimeout(load,1);});\n"
        "})();\n"
        "</script>\n"
    )


def fonts_head() -> str:
    """LCP-first font hints: preload display face only; inline @font-face (no blocking CSS)."""
    fonts_css = (ROOT / "assets" / "fonts.css").read_text(encoding="utf-8").strip()
    return (
        '<style>html,body{background:#1A1A1A;color:#F1EEE7}</style>\n'
        '<link rel="preload" href="/assets/fonts/big-shoulders-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<link rel="preload" href="/assets/fonts/big-shoulders-latin-ext.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<link rel="preload" href="/assets/fonts/inter-latin-ext.woff2" as="font" type="font/woff2" crossorigin>\n'
        f"<style>\n{fonts_css}\n</style>\n"
    )


A0 = {
    "tabela": "Tabela",
    "isikli-tabela": "Işıklı Tabela",
    "kutu-harf": "Kutu Harf",
    "totem": "Totem",
    "arac-giydirme": "Araç Giydirme",
    "cam-giydirme": "Cam Giydirme",
}
A2 = {
    "lightbox": "Lightbox",
    "display-pos": "Display & POS",
    "ofis-branding": "Ofis Branding",
    "is-guvenligi-tabelalari": "İş Güvenliği Tabelaları",
}
ALL_SERVICES = {**A0, **A2}


def wa(msg: str) -> str:
    return f"https://wa.me/{WA}?text={quote(msg)}"


def logo() -> str:
    return (
        '<img class="logo-mark" src="/images/logo.svg" width="120" height="19" '
        'alt="Malt Studio">'
    )


THEME_BOOT = (
    "<script>"
    "(function(){try{"
    "var t=localStorage.getItem('malt-theme');"
    "var r=document.documentElement;"
    "if(t==='light')r.setAttribute('data-theme','light');"
    "else if(t==='liquid')r.classList.add('liquid-glass');"
    "}catch(e){}})();"
    "</script>\n"
)

THEME_TOGGLE = (
    '<button type="button" class="theme-toggle" data-theme-toggle '
    'aria-pressed="false" aria-label="Açık arayüze geç" title="Koyu" '
    'data-theme-current="dark">'
    '<svg class="icon-moon" viewBox="0 0 24 24" aria-hidden="true" fill="none" '
    'stroke="currentColor" stroke-width="1.75">'
    '<path d="M20.2 14.3A8.5 8.5 0 0 1 9.7 3.8 7 7 0 1 0 20.2 14.3z"/>'
    "</svg>"
    '<svg class="icon-sun" viewBox="0 0 24 24" aria-hidden="true" fill="none" '
    'stroke="currentColor" stroke-width="1.75">'
    '<circle cx="12" cy="12" r="4"/>'
    '<path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2'
    'M5.4 5.4l1.6 1.6M17 17l1.6 1.6M18.6 5.4 17 7M7 17l-1.6 1.6"/>'
    "</svg>"
    '<svg class="icon-glass" viewBox="0 0 24 24" aria-hidden="true" fill="none" '
    'stroke="currentColor" stroke-width="1.75">'
    '<circle cx="12" cy="12" r="7"/>'
    '<path d="M8.5 11.5c1.2-2.2 3-3.5 3.5-3.5s2.3 1.3 3.5 3.5"/>'
    '<path d="M9 15.5c.8.9 1.9 1.5 3 1.5s2.2-.6 3-1.5"/>'
    "</svg>"
    "</button>"
)


def theme_script() -> str:
    return '<script src="/assets/theme.js?v=theme2" defer></script>\n'


def ld_script(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f'<script type="application/ld+json">{payload}</script>\n'


def business_ref() -> dict:
    return {"@id": f"{SITE}/#business"}


def breadcrumb_ld(parts: list[tuple[str, str]]) -> dict:
    """parts: (name, absolute_or_path url). Last item is the current page."""
    items = []
    for i, (name, url) in enumerate(parts, 1):
        loc = url if url.startswith("http") else f"{SITE}{url}"
        items.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": name,
                "item": loc,
            }
        )
    return {
        "@type": "BreadcrumbList",
        "@id": f"{parts[-1][1] if parts[-1][1].startswith('http') else SITE + parts[-1][1]}#breadcrumb",
        "itemListElement": items,
    }


def webpage_ld(url: str, name: str, description: str) -> dict:
    return {
        "@type": "WebPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": name,
        "description": description,
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": business_ref(),
        "inLanguage": "tr-TR",
    }


def service_ld(url: str, name: str, service_type: str) -> dict:
    return {
        "@type": "Service",
        "@id": f"{url}#service",
        "name": name,
        "serviceType": service_type,
        "url": url,
        "provider": business_ref(),
        "areaServed": [
            {"@type": "City", "name": "Tekirdağ"},
            {"@type": "AdministrativeArea", "name": "Süleymanpaşa"},
        ],
    }


def page_graph(*nodes: dict) -> dict:
    return {"@context": "https://schema.org", "@graph": [n for n in nodes if n]}


def head(
    title: str,
    description: str,
    canonical: str,
    *,
    noindex: bool = False,
    nofollow: bool = False,
    json_ld: dict | None = None,
) -> str:
    # Tracking pages use noindex,nofollow; other noindex pages keep follow.
    if noindex and nofollow:
        robots_content = "noindex, nofollow"
    elif noindex:
        robots_content = "noindex, follow"
    else:
        robots_content = "index, follow"
    robots = f'<meta name="robots" content="{robots_content}">\n'
    ga = gtag_snippet()
    ld = ld_script(json_ld) if json_ld else ""
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{THEME_BOOT}{ga}<title>{title}</title>
<meta name="description" content="{description}">
{robots}<link rel="canonical" href="{canonical}">
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
{fonts_head()}<link rel="stylesheet" href="/assets/site.css?v=theme2">
<link rel="stylesheet" href="/assets/liquid-glass.css?v=lg1">
{ld}</head>
"""


def header() -> str:
    return f"""<header>
  <a href="/" aria-label="Malt Studio">{logo()}</a>
  <div class="header-actions">
    <nav aria-label="Ana menü">
      <a href="/#teklif">Teklif</a>
      <a href="/#iletisim">İletişim</a>
    </nav>
    {THEME_TOGGLE}
  </div>
</header>
<main>
"""


def footer() -> str:
    svc = "\n".join(
        f'<li><a href="/hizmetler/{s}/">{n}</a></li>' for s, n in ALL_SERVICES.items()
    )
    return f"""</main>
<footer>
  <div class="wrap">
    <div class="footer-top">
      <div>
        <div class="footer-logo">{logo()}</div>
        <p class="footer-blurb">
          Malt Studio — Tekirdağ merkezli reklam ve tabela üreticisi. Üretim, montaj ve marka görünürlüğü.
        </p>
      </div>
      <div>
        <h3>Hizmetler</h3>
        <ul>{svc}</ul>
      </div>
      <div>
        <h3>Keşif</h3>
        <ul>
          <li><a href="/projeler/">Projeler</a></li>
          <li><a href="/sektorler/">Sektörler</a></li>
          <li><a href="/bilgi/">Bilgi</a></li>
          <li><a href="/bolgeler/tekirdag/">Tekirdağ</a></li>
          <li><a href="/hizmetler/">Tüm hizmetler</a></li>
        </ul>
      </div>
      <div>
        <h3>İletişim</h3>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ADDRESS_STREET}</li>
          <li>{ADDRESS_POSTAL} {ADDRESS_LOCALITY} / {ADDRESS_REGION}</li>
          <li>{ADDRESS_COUNTRY}</li>
          <li><a href="/#iletisim">Mesaj</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2025–2026 Malt Studio</span>
    </div>
  </div>
</footer>
<a class="whatsapp-btn" href="{wa("Merhaba, Malt Studio hizmetleri hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener" aria-label="WhatsApp ile iletişime geç">WhatsApp</a>
{theme_script()}"""


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


def cards(items: list[tuple[str, str, str, str]]) -> str:
    """href, title, desc, meta"""
    return "\n".join(
        f'<a class="card" href="{href}"><h3>{title}</h3><p>{desc}</p>'
        f'<span class="meta">{meta}</span></a>'
        for href, title, desc, meta in items
    )


def cta_band(title: str, msg: str) -> str:
    return f"""<section class="cta-band">
  <div class="wrap">
    <h2>{title}</h2>
    <p class="intro" style="margin:0 auto 28px;text-align:center;">Keşif, ölçü ve net teklif için yazın veya arayın.</p>
    <div class="cta-actions" style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
      <a class="btn btn-primary" href="{wa(msg)}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
      <a class="btn btn-ghost" href="/#teklif">Teklif</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Ara: {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>
"""


def project_cta(name: str) -> str:
    """Wave A4 conversion block: Teklif Al · WhatsApp · Telefon."""
    msg = f"Merhaba, {name} benzeri bir proje için teklif almak istiyorum."
    return f"""<section class="cta-band" aria-labelledby="project-cta-title">
  <div class="wrap">
    <h2 id="project-cta-title">Benzer bir proje konuşalım</h2>
    <p class="intro" style="margin:0 auto 28px;text-align:center;">Keşif ve net teklif için yazın veya arayın. Uydurma süre/fiyat vaadi verilmez.</p>
    <div class="cta-actions" style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
      <a class="btn btn-primary" href="/#teklif">Teklif Al</a>
      <a class="btn btn-ghost" href="{wa(msg)}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Telefon · {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>
"""


def evidence_gallery(project_name: str) -> str:
    """Responsive placeholder slots for future real photos. No fabricated images."""
    slots = [
        ("gallery", "Proje galerisi", "Onaylı saha ve teslim fotoğrafları eklenecek."),
        ("before-after", "Before / After", "Önce–sonra karşılaştırması onay sonrası eklenecek."),
        ("installation", "Montaj fotoğrafları", "Kurulum günü görselleri bekleniyor."),
        ("workshop", "Atölye fotoğrafları", "Üretim süreci görselleri bekleniyor."),
        ("materials", "Malzeme close-up", "Yüzey/malzeme detay fotoğrafları bekleniyor."),
    ]
    figs = []
    for key, label, note in slots:
        figs.append(
            f'<figure class="evidence-slot" data-evidence="{key}">'
            f'<div class="evidence-frame" role="img" aria-label="{label} — yer tutucu">'
            f'<span class="evidence-label">{label}</span>'
            f'<span class="evidence-note">{note}</span>'
            f"</div>"
            f"<figcaption>{project_name} · {label} · proje verisi bekleniyor</figcaption>"
            f"</figure>"
        )
    return (
        '<section class="section-band" aria-labelledby="evidence-title">'
        '<div class="wrap">'
        '<h2 id="evidence-title">Proje görselleri</h2>'
        '<p class="intro">Gerçek fotoğraflar eklenene kadar yer tutucu çerçeveler gösteriliyor.</p>'
        f'<div class="evidence-grid">{"".join(figs)}</div>'
        "</div></section>"
    )


def mid_cta(msg: str) -> str:
    """In-section conversion row reused across hizmet / bölge / bilgi pages."""
    return f"""<div class="content-block page-mid-cta">
  <p><a class="btn btn-primary" href="{wa(msg)}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
  <a class="btn btn-ghost" href="/#teklif" style="margin-left:10px;">Teklif</a>
  <a class="btn btn-ghost" href="tel:{PHONE_TEL}" style="margin-left:10px;">Ara</a></p>
</div>"""


def eeat_block(page_type: str) -> str:
    return f"""<div class="content-block">
  <h2>Üretim, deneyim ve yerel uzmanlık</h2>
  <p>Malt Studio Tekirdağ merkezli çalışır. Bu {page_type} içeriği; atölye üretimi, saha keşfi ve montajın aynı operasyonel hatta planlandığı gerçek iş modeline dayanır. Şube sayısı, uydurma sertifika, sahte yorum veya proje metriği eklenmez.</p>
  <ul>
    <li><strong>Deneyim:</strong> Keşif notları (ölçü, yüzey, erişim, işletme saati) teklif ve üretimi şekillendirir.</li>
    <li><strong>Üretim:</strong> Ölçüye özel imalat; stok tabela mantığı yerine yüzeye ve markaya göre üretim.</li>
    <li><strong>Kalite süreci:</strong> Atölye kontrolü → saha hizalama/sabitleme → teslim kontrolü.</li>
    <li><strong>Yerel uzmanlık:</strong> Tekirdağ üssünden merkez ve çevre ilçe işleri planlanır; Süleymanpaşa dahil merkez ve çevre ilçelere hizmet verilir.</li>
    <li><strong>Kanıt:</strong> Gerçek fotoğraflar proje sayfalarına bağlanır; stok görsel kullanılmaz.</li>
  </ul>
</div>"""


def related_rail(
    *,
    services: list[tuple[str, str, str]] | None = None,
    knowledge: list[tuple[str, str, str]] | None = None,
    projects: list[str] | None = None,
    industries: list[tuple[str, str, str]] | None = None,
    hubs: list[tuple[str, str, str]] | None = None,
) -> str:
    """Consistent internal-link sections. tuples: (href, title, desc)."""
    # Dedicated case URLs are placeholders — do not link them from indexable pages.
    names: dict[str, str] = {}
    parts: list[str] = []
    if services:
        parts.append(
            '<section class="section-band paper-band" aria-labelledby="rel-svc">'
            '<div class="wrap"><h2 id="rel-svc">İlgili hizmetler</h2>'
            f'<div class="card-grid">{cards([(h,t,d,"Hizmet") for h,t,d in services])}</div>'
            "</div></section>"
        )
    if knowledge:
        parts.append(
            '<section class="section-band" aria-labelledby="rel-bil">'
            '<div class="wrap"><h2 id="rel-bil">İlgili rehberler</h2>'
            f'<div class="card-grid">{cards([(h,t,d,"Bilgi") for h,t,d in knowledge])}</div>'
            "</div></section>"
        )
    if projects:
        items = [
            (f"/projeler/{s}/", names[s], "Tamamlanan proje örneği.", "Proje")
            for s in projects
            if s in names
        ]
        if items:
            parts.append(
                '<section class="section-band paper-band" aria-labelledby="rel-prj">'
                '<div class="wrap"><h2 id="rel-prj">İlgili projeler</h2>'
                f'<div class="card-grid">{cards(items)}</div>'
                '<p style="margin-top:20px;"><a href="/projeler/">Tüm projeler →</a></p>'
                "</div></section>"
            )
    if industries:
        parts.append(
            '<section class="section-band" aria-labelledby="rel-ind">'
            '<div class="wrap"><h2 id="rel-ind">İlgili sektörler</h2>'
            f'<div class="card-grid">{cards([(h,t,d,"Sektör") for h,t,d in industries])}</div>'
            "</div></section>"
        )
    if hubs is None:
        hubs = [
            ("/hizmetler/", "Hizmetler", "Tüm hizmetlerimize göz atın."),
            ("/bilgi/", "Bilgi", "Rehberler ve karar içerikleri."),
            ("/projeler/", "Projeler", "Tamamladığımız işlerden örnekler."),
            ("/sektorler/", "Sektörler", "Sektöre özel çözümler."),
            ("/bolgeler/tekirdag/", "Tekirdağ", "Tekirdağ yerel hizmet rehberi."),
            ("/", "Ana sayfa", "Malt Studio ana sayfa."),
        ]
    if hubs:
        parts.append(
            '<section class="section-band paper-band" aria-labelledby="rel-hub">'
            '<div class="wrap"><h2 id="rel-hub">Keşfet</h2>'
            f'<div class="card-grid">{cards([(h,t,d,"Keşif") for h,t,d in hubs])}</div>'
            "</div></section>"
        )
    return "\n".join(parts)


def process_steps(steps: list[tuple[str, str]], title: str = "Süreç") -> str:
    lis = "".join(f"<li><strong>{t}:</strong> {d}</li>" for t, d in steps)
    return f"""<div class="content-block">
  <h2>{title}</h2>
  <ol>{lis}</ol>
</div>"""


def project_placeholders(slugs: list[str]) -> str:
    names = {
        "liman-kahve": "Liman Kahve",
        "volt-enerji": "Volt Enerji",
        "kuzey-tekstil": "Kuzey Tekstil",
        "mera-otel": "Mera Otel",
        "dortnal": "Dörtnal",
        "ekip-yazilim": "Ekip Yazılım",
    }
    items = [
        (
            f"/projeler/{s}/",
            names.get(s, s),
            "Vaka sayfası — görseller onaylandıkça güncellenir.",
            "Proje",
        )
        for s in slugs
    ]
    return f"""<section class="section-band paper-band">
  <div class="wrap">
    <h2>İlgili proje örnekleri</h2>
    <p class="intro">Kanıt katmanı. Fotoğraflar eklenene kadar proje sayfaları noindex ile tutulabilir.</p>
    <div class="card-grid">{cards(items)}</div>
    <p style="margin-top:20px;"><a href="/projeler/">Tüm projeler →</a></p>
  </div>
</section>"""


def write(path: Path, html: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))
