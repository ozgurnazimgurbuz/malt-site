#!/usr/bin/env python3
"""Shared shell, CTAs, EEAT blocks for production page builds."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://maltstudio.co"
PHONE_DISPLAY = "0552 582 69 59"
PHONE_TEL = "+905525826959"
WA = "905525826959"
EMAIL = "merhaba@maltstudio.com"
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
    """Single Google tag (gtag.js) block for <head>. Empty when ID missing."""
    ga_id = (ga_id or google_analytics_id()).strip()
    if not _GA_ID_RE.match(ga_id):
        return ""
    return (
        "<!-- Google tag (gtag.js) -->\n"
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>\n'
        "<script>\n"
        "  window.dataLayer = window.dataLayer || [];\n"
        "  function gtag(){dataLayer.push(arguments);}\n"
        "  gtag('js', new Date());\n"
        f"  gtag('config', '{ga_id}');\n"
        "</script>\n"
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


def head(
    title: str,
    description: str,
    canonical: str,
    *,
    noindex: bool = False,
) -> str:
    robots = (
        '<meta name="robots" content="noindex,follow">\n'
        if noindex
        else '<meta name="robots" content="index,follow">\n'
    )
    ga = gtag_snippet()
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{ga}<title>{title}</title>
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
"""


def header() -> str:
    return f"""<header>
  <a href="/" aria-label="Malt Studio">{logo()}</a>
  <nav>
    <a href="/hizmetler/">Hizmetler</a>
    <a href="/projeler/">Projeler</a>
    <a href="/sektorler/">Sektörler</a>
    <a href="/bilgi/">Bilgi</a>
    <a href="/bolgeler/tekirdag/">Tekirdağ</a>
    <a href="/#iletisim">İletişim</a>
  </nav>
</header>
"""


def footer() -> str:
    svc = "\n".join(
        f'<li><a href="/hizmetler/{s}/">{n}</a></li>' for s, n in ALL_SERVICES.items()
    )
    return f"""<footer>
  <div class="wrap">
    <div class="footer-top">
      <div>
        <div class="footer-logo">{logo()}</div>
        <p style="font-size:14px;line-height:1.65;color:rgba(241,238,231,0.65);max-width:300px;">
          Malt Studio — Tekirdağ merkezli reklam ve tabela üreticisi. Üretim, montaj ve marka görünürlüğü.
        </p>
      </div>
      <div>
        <h4>Hizmetler</h4>
        <ul>{svc}</ul>
      </div>
      <div>
        <h4>Keşif</h4>
        <ul>
          <li><a href="/projeler/">Projeler</a></li>
          <li><a href="/sektorler/">Sektörler</a></li>
          <li><a href="/bilgi/">Bilgi</a></li>
          <li><a href="/bolgeler/tekirdag/">Tekirdağ</a></li>
          <li><a href="/hizmetler/">Tüm hizmetler</a></li>
        </ul>
      </div>
      <div>
        <h4>İletişim</h4>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Tekirdağ, Türkiye</li>
          <li><a href="/#iletisim">Mesaj</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2025–2026 Malt Studio</span>
      <span>Production content layer</span>
    </div>
  </div>
</footer>
<a class="whatsapp-btn" href="{wa("Merhaba, Malt Studio hizmetleri hakkında bilgi almak istiyorum.")}" target="_blank" rel="noopener">WhatsApp</a>
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
    <a class="btn btn-primary" href="{wa(msg)}" target="_blank" rel="noopener">WhatsApp ile Teklif</a>
    <a class="btn btn-ghost" href="tel:{PHONE_TEL}" style="margin-left:12px;">Ara: {PHONE_DISPLAY}</a>
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
      <a class="btn btn-primary" href="{wa(msg)}" target="_blank" rel="noopener">Teklif Al</a>
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
        '<h2 id="evidence-title">Kanıt görselleri</h2>'
        '<p class="intro">EEAT kapısı: gerçek fotoğraflar gelene kadar yer tutucu çerçeveler. Stok veya uydurma görsel kullanılmaz. Sayfa noindex,follow kalır.</p>'
        f'<div class="evidence-grid">{"".join(figs)}</div>'
        "</div></section>"
    )


def mid_cta(msg: str) -> str:
    return f"""<div class="content-block">
  <p><a class="btn btn-primary" href="{wa(msg)}" target="_blank" rel="noopener">WhatsApp</a>
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
  <p class="note">EEAT kapısı açıktır: görseller ve onaylı vakalar geldikçe ilgili proje URL’leri güçlenir. Proje sayfaları kanıt yetersizken noindex,follow kalabilir.</p>
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
    names = {
        "liman-kahve": "Liman Kahve",
        "volt-enerji": "Volt Enerji",
        "kuzey-tekstil": "Kuzey Tekstil",
        "mera-otel": "Mera Otel",
        "dortnal": "Dörtnal",
        "ekip-yazilim": "Ekip Yazılım",
    }
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
            (f"/projeler/{s}/", names.get(s, s), "Tamamlanan proje örneği.", "Proje")
            for s in projects
        ]
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
            '<div class="wrap"><h2 id="rel-hub">Hub bağlantıları</h2>'
            f'<div class="card-grid">{cards([(h,t,d,"Hub") for h,t,d in hubs])}</div>'
            "</div></section>"
        )
    return "\n".join(parts)


def process_steps(steps: list[tuple[str, str]]) -> str:
    lis = "".join(f"<li><strong>{t}:</strong> {d}</li>" for t, d in steps)
    return f"""<div class="content-block">
  <h2>Süreç</h2>
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
