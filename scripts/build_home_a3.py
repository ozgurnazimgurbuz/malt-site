#!/usr/bin/env python3
"""Wave A3 — Homepage authority upgrade. No new URLs."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

WA = (
    "https://wa.me/905525826959?"
    "text=Merhaba%2C%20teklif%20almak%20istiyorum."
)
WA_API = (
    "https://api.whatsapp.com/send?phone=905525826959&"
    "text=Merhaba%2C%20teklif%20almak%20istiyorum."
)
PHONE_TEL = "+905525826959"

A3_CSS = """
  /* -------- A3 home authority -------- */
  .hero{
    justify-content:flex-start;
    padding:108px 0 80px;
    isolation:isolate;
  }
  .rings{z-index:-1;}
  .hero .wrap{
    position:relative; z-index:1;
    width:100%; max-width:1240px;
    margin-left:0; margin-right:auto;
    padding-left:56px; padding-right:56px;
  }
  .hero .scroll-cue{z-index:1; left:56px;}
  .hero h1{line-height:1.08;}
  .section-head h2{line-height:1.08;}
  /* Section intros: --muted (0.62) reads too dim on mobile OLED */
  .section-head p{color:var(--muted-chip);}
  /* Logo already brands the page — drop redundant eyebrow brand on all viewports. */
  #hero-eyebrow .eyebrow-brand{display:none;}
  .trust-strip{
    border-top:1px solid var(--line); border-bottom:1px solid var(--line);
    padding:28px 0; background:var(--trust-wash);
  }
  .trust-strip ul{
    list-style:none; display:flex; flex-wrap:wrap; gap:12px 28px;
    justify-content:space-between; align-items:center;
    font-size:12px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase;
    color:var(--paper);
  }
  .trust-strip li{display:flex; align-items:center; gap:10px; white-space:nowrap;}
  .trust-strip li::before{
    content:''; width:7px; height:7px; border-radius:1px; background:var(--taupe); flex-shrink:0;
  }
  .service-grid.enterprise{grid-template-columns:repeat(3,1fr);}
  .service-card{min-height:200px;}
  .chip-grid{
    display:flex; flex-wrap:wrap; gap:12px;
  }
  .chip{
    display:inline-flex; align-items:center;
    padding:12px 16px; border:1px solid var(--line);
    font-size:13px; font-weight:600; letter-spacing:0.04em;
    color:var(--muted-chip); transition:border-color .2s, color .2s, background .2s;
  }
  a.chip:hover{border-color:var(--taupe); color:var(--paper); background:rgba(176,141,114,0.08);}
  .chip.is-alias{opacity:0.72; border-style:dashed;}
  .process-grid{
    display:grid; grid-template-columns:repeat(6,1fr); gap:1px;
    background:var(--line); border:1px solid var(--line);
  }
  .process-step{
    background:var(--ink); padding:28px 20px; min-height:160px;
    display:flex; flex-direction:column; gap:12px;
  }
  .process-step .num{
    font-family:'Big Shoulders Display','Big Shoulders Fallback',sans-serif; font-weight:900;
    font-size:15px; color:var(--maroon-light);
  }
  .process-step h3{
    font-size:20px; text-transform:none; letter-spacing:0; line-height:1.15;
  }
  .process-step p{font-size:13px; line-height:1.55; color:var(--muted);}
  .why-grid{
    display:grid; grid-template-columns:repeat(5,1fr); gap:1px;
    background:var(--line); border:1px solid var(--line);
  }
  .why-card{
    background:var(--ink); padding:28px 22px; min-height:180px;
  }
  .why-card h3{
    font-size:20px; text-transform:none; letter-spacing:0; line-height:1.2; margin-bottom:12px;
  }
  .why-card p{font-size:14px; line-height:1.55; color:var(--muted);}
  .knowledge-grid{
    display:grid; grid-template-columns:repeat(3,1fr); gap:1px;
    background:rgba(26,26,26,0.14); border:1px solid rgba(26,26,26,0.14);
  }
  .knowledge-card{
    background:var(--paper); padding:28px 24px; min-height:160px;
    display:flex; flex-direction:column; gap:10px; color:inherit; transition:background .2s;
  }
  a.knowledge-card:hover{background:#e6dccb;}
  .knowledge-card .meta{
    font-size:11px; letter-spacing:0.12em; text-transform:uppercase; color:var(--maroon); font-weight:700;
  }
  .knowledge-card h3{
    font-size:22px; text-transform:none; letter-spacing:0; line-height:1.15; margin-top:auto;
  }
  .knowledge-card p{font-size:14px; color:var(--ink-soft); line-height:1.55;}
  .cta-actions{display:flex; gap:16px; justify-content:center; flex-wrap:wrap; margin-top:8px;}
  .section-link{
    font-size:13px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;
    color:var(--taupe); border-bottom:1px solid transparent;
  }
  .section-link:hover{border-color:var(--taupe);}
  .services .section-link{color:var(--maroon);}
  a.work-item{color:inherit;}
  @media (max-width:1100px){
    .process-grid{grid-template-columns:repeat(3,1fr);}
    .why-grid{grid-template-columns:repeat(3,1fr);}
  }
  @media (max-width:900px){
    .service-grid.enterprise{grid-template-columns:repeat(2,1fr);}
    .knowledge-grid{grid-template-columns:1fr 1fr;}
    .why-grid{grid-template-columns:1fr 1fr;}
    .trust-strip ul{justify-content:flex-start;}
  }
  @media (max-width:560px){
    .process-grid{grid-template-columns:1fr 1fr;}
    .knowledge-grid{grid-template-columns:1fr;}
    .why-grid{grid-template-columns:1fr;}
    .service-grid.enterprise{grid-template-columns:1fr;}
    .hero .wrap{padding-left:20px; padding-right:20px;}
    .hero .scroll-cue{left:20px;}
  }
"""

MAIN = f"""
<section class="hero" aria-label="Giriş">
  <svg class="rings" viewBox="0 0 800 800" aria-hidden="true">
    <circle cx="400" cy="400" r="90"/>
    <circle cx="400" cy="400" r="180"/>
    <circle cx="400" cy="400" r="270"/>
    <circle cx="400" cy="400" r="360"/>
    <circle cx="400" cy="400" r="400"/>
  </svg>
  <div class="wrap">
    <div class="eyebrow" id="hero-eyebrow"><span class="eyebrow-brand">Malt Studio · </span>Tekirdağ Reklam Ajansı</div>
    <h1 id="hero-title">Markanızı <span id="hero-highlight">sahada</span><br id="hero-br">görünür kılarız.</h1>
    <p class="hero-sub" id="hero-sub">Tabela üretimi, kurumsal kimlik, dijital baskı ve uygulama. Keşiften montaja Tekirdağ merkezli üretim.</p>
    <div class="hero-actions">
      <a href="#teklif" class="btn btn-primary" id="cta-primary">Teklif Al</a>
      <a href="{WA}" class="btn btn-ghost" id="cta-secondary" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
  <div class="scroll-cue">Aşağı kaydır</div>
</section>

<section class="trust-strip" aria-label="Güven özeti">
  <div class="wrap">
    <ul>
      <li>Yerinde Keşif</li>
      <li>Tasarım</li>
      <li>Üretim</li>
      <li>Montaj</li>
      <li>Tek Noktadan Hizmet</li>
    </ul>
  </div>
</section>

<section id="isler" aria-labelledby="portfolio-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="tag" id="portfolio-tag">Projeler</div>
        <h2 id="portfolio-title">Seçili İşler</h2>
      </div>
      <p id="portfolio-intro">Tamamladığımız işlerden öne çıkanlar.</p>
    </div>
  </div>
  <div class="work-grid" id="work-grid"></div>
  <div class="wrap" style="margin-top:28px;"><a class="section-link" href="/projeler/">Tüm projeler →</a></div>
</section>

<section class="services" id="hizmetler" aria-labelledby="services-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="tag" id="services-tag">Hizmetler</div>
        <h2 id="services-title">Çekirdek<br>Hizmetler</h2>
      </div>
      <p id="services-intro">Üretimden montaja, ihtiyacınıza uygun çözümler.</p>
    </div>
    <div class="service-grid enterprise" id="service-grid"></div>
    <p style="margin-top:28px;"><a class="section-link" href="/hizmetler/">Tüm hizmetler →</a></p>
  </div>
</section>

<section id="sektorler" aria-labelledby="industries-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="tag">Sektörler</div>
        <h2 id="industries-title">Çalıştığımız<br>Sektörler</h2>
      </div>
      <p>Farklı sektörlere özel çözümler sunuyoruz.</p>
    </div>
    <div class="local-grid">
      <a class="local-card" href="/sektorler/fabrika-osb/"><h3>Fabrikalar / OSB</h3><p>Tesis kimliği, totem ve iş güvenliği.</p><span class="meta">Sektör</span></a>
      <a class="local-card" href="/sektorler/perakende/"><h3>Perakende</h3><p>Mağaza cephe ve vitrin.</p><span class="meta">Sektör</span></a>
      <a class="local-card" href="/sektorler/restoran-cafe/"><h3>Restoran / Cafe</h3><p>Tabela, cam ve menü yüzeyleri.</p><span class="meta">Sektör</span></a>
      <a class="local-card" href="/sektorler/plaza-ofis/"><h3>Plaza / Ofis</h3><p>Ofis branding ve giriş kimliği.</p><span class="meta">Sektör</span></a>
      <a class="local-card" href="/sektorler/insaat-santiye/"><h3>İnşaat / Şantiye</h3><p>Geçici ve kalıcı saha işaretleri.</p><span class="meta">Sektör</span></a>
      <a class="local-card" href="/sektorler/saglik/"><h3>Sağlık</h3><p>Klinik ve sağlık noktası görünürlüğü.</p><span class="meta">Sektör</span></a>
    </div>
    <p style="margin-top:28px;"><a class="section-link" href="/sektorler/">Tüm sektörler →</a></p>
  </div>
</section>

<section id="surec" aria-labelledby="process-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="tag">Süreç</div>
        <h2 id="process-title">Üretim<br>Süreci</h2>
      </div>
      <p>Keşiften teslimata kadar birlikte yürüdüğümüz süreç.</p>
    </div>
    <div class="process-grid">
      <div class="process-step"><div class="num">01</div><h3>Keşif</h3><p>Ölçü, yüzey ve saha koşulları yerinde not edilir.</p></div>
      <div class="process-step"><div class="num">02</div><h3>Tasarım</h3><p>Okunur, markaya uygun görsel onaylanır.</p></div>
      <div class="process-step"><div class="num">03</div><h3>Üretim</h3><p>Atölyede ölçüye özel imalat.</p></div>
      <div class="process-step"><div class="num">04</div><h3>Kalite Kontrol</h3><p>Montaj öncesi ölçü ve bitiş kontrolü.</p></div>
      <div class="process-step"><div class="num">05</div><h3>Montaj</h3><p>Sahada güvenli uygulama ve teslim.</p></div>
      <div class="process-step"><div class="num">06</div><h3>Satış Sonrası</h3><p>Servis ve yenileme talepleri aynı hattan.</p></div>
    </div>
    <p style="margin-top:28px;"><a class="section-link" href="#surec">Süreç özeti (bu sayfa) →</a></p>
  </div>
</section>

<section class="services" id="bilgi" aria-labelledby="knowledge-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="tag">Bilgi</div>
        <h2 id="knowledge-title">Bilgi<br>Merkezi</h2>
      </div>
      <p>Karar vermenize yardımcı olacak rehberler.</p>
    </div>
    <div class="knowledge-grid">
      <a class="knowledge-card" href="/bilgi/tabela-cesitleri/"><span class="meta">Rehber</span><h3>Tabela Çeşitleri</h3><p>Hangi tabela tipi ne zaman seçilir.</p></a>
      <a class="knowledge-card" href="/bilgi/isikli-mi-isiksiz-mi/"><span class="meta">Karar</span><h3>Işıklı mı Işıksız mı?</h3><p>Gece görünürlük ihtiyacını netleştirin.</p></a>
      <a class="knowledge-card" href="/bilgi/kutu-harf-malzemeler/"><span class="meta">Malzeme</span><h3>Kutu Harf Malzemeler</h3><p>Pleksi, paslanmaz ve seçim kriterleri.</p></a>
      <a class="knowledge-card" href="/bilgi/one-way-vision-nedir/"><span class="meta">Cam</span><h3>One Way Vision Nedir?</h3><p>Vitrin folyo mantığı.</p></a>
      <a class="knowledge-card" href="/bilgi/arac-giydirme-rehberi/"><span class="meta">Filo</span><h3>Araç Giydirme Rehberi</h3><p>Kaplama öncesi bilmeniz gerekenler.</p></a>
      <a class="knowledge-card" href="/bilgi/totem-secim-rehberi/"><span class="meta">Tesis</span><h3>Totem Seçim Rehberi</h3><p>Yol ve giriş totem kararları.</p></a>
    </div>
    <p style="margin-top:28px;"><a class="section-link" href="/bilgi/">Tüm rehberler →</a></p>
    <div class="cta-actions" style="justify-content:flex-start;margin-top:20px;">
      <a href="#teklif" class="btn btn-primary">Teklif Al</a>
      <a href="{WA}" class="btn btn-ghost" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>

<section id="neden" aria-labelledby="why-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="tag">Neden Biz</div>
        <h2 id="why-title">Neden<br>Malt Studio</h2>
      </div>
      <p>Üreten ekip, sahada montaj, kurumsal yaklaşım ve yerel destek.</p>
    </div>
    <div class="why-grid">
      <div class="why-card"><h3>Gerçek üretim</h3><p>Atölyede ölçüye özel imalat. Stok tabela mantığı yerine yüzeye ve markaya göre üretim.</p></div>
      <div class="why-card"><h3>Modern ekipman</h3><p>Dijital baskı ve tabela üretim hatları güncel ihtiyaçlara göre kullanılır.</p></div>
      <div class="why-card"><h3>Montaj deneyimi</h3><p>Keşif, lojistik ve saha uygulaması aynı operasyonel hatta planlanır.</p></div>
      <div class="why-card"><h3>Kurumsal yaklaşım</h3><p>Brief, onay, yazılı teklif ve teslim kontrolü ile ilerleriz.</p></div>
      <div class="why-card"><h3>Yerel destek</h3><p>Tekirdağ üssünden çevre ilçelere keşif ve servis.</p></div>
    </div>
  </div>
</section>

<section id="bolge" aria-labelledby="coverage-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="tag">Kapsama</div>
        <h2 id="coverage-title">Hizmet<br>Bölgesi</h2>
      </div>
      <p>Tekirdağ merkezliyiz; çevre ilçe ve komşu illere keşif ve montaj desteği sunuyoruz.</p>
    </div>
    <div class="chip-grid" aria-label="Hizmet verilen bölgeler">
      <a class="chip" href="/bolgeler/tekirdag/">Tekirdağ</a>
      <span class="chip">Çorlu</span>
      <span class="chip">Çerkezköy</span>
      <span class="chip">Kapaklı</span>
      <span class="chip">Ergene</span>
      <span class="chip">Şarköy</span>
      <span class="chip">Muratlı</span>
      <span class="chip">Malkara</span>
      <span class="chip">Hayrabolu</span>
      <span class="chip">Saray</span>
      <span class="chip">Marmara Ereğlisi</span>
      <a class="chip" href="/bolgeler/tekirdag/">Süleymanpaşa</a>
      <span class="chip">İstanbul</span>
      <span class="chip">Edirne</span>
      <span class="chip">Çanakkale</span>
      <span class="chip">Kırklareli</span>
    </div>
    <div class="local-grid" style="margin-top:40px;">
      <a class="local-card" href="/bolgeler/tekirdag/"><h3>Tekirdağ Reklam Ajansı</h3><p>Tekirdağ’da tabela üretimi, keşif ve montaj — yerel hizmet rehberi.</p><span class="meta">Yerel</span></a>
      <a class="local-card" href="/hizmet-bolge/tekirdag-tabela/"><h3>Tekirdağ Tabela</h3><p>Tekirdağ’da tabela üretimi ve montajı.</p><span class="meta">Yerel</span></a>
      <a class="local-card" href="/hizmet-bolge/tekirdag-isikli-tabela/"><h3>Tekirdağ Işıklı</h3><p>Tekirdağ’da ışıklı tabela hizmeti.</p><span class="meta">Yerel</span></a>
      <a class="local-card" href="/hizmet-bolge/tekirdag-kutu-harf/"><h3>Tekirdağ Kutu Harf</h3><p>Tekirdağ’da kutu harf üretimi.</p><span class="meta">Yerel</span></a>
      <a class="local-card" href="/hizmet-bolge/tekirdag-totem/"><h3>Tekirdağ Totem</h3><p>Tekirdağ’da totem tabela uygulamaları.</p><span class="meta">Yerel</span></a>
      <a class="local-card" href="/hizmet-bolge/tekirdag-arac-giydirme/"><h3>Tekirdağ Araç</h3><p>Tekirdağ’da araç giydirme hizmeti.</p><span class="meta">Yerel</span></a>
      <a class="local-card" href="/hizmet-bolge/tekirdag-cam-giydirme/"><h3>Tekirdağ Cam</h3><p>Tekirdağ’da cam giydirme uygulamaları.</p><span class="meta">Yerel</span></a>
      <a class="local-card" href="/projeler/"><h3>Projeler</h3><p>Tekirdağ’da seçili tabela ve uygulama işleri.</p><span class="meta">Keşif</span></a>
      <a class="local-card" href="/hizmetler/"><h3>Tüm Hizmetler</h3><p>Tüm hizmetlerimize göz atın.</p><span class="meta">Hizmet</span></a>
    </div>
  </div>
</section>

<section id="kultur" aria-label="Özet göstergeler">
  <div class="wrap">
    <div class="stats" id="stats-grid"></div>
  </div>
</section>

<section class="cta" id="teklif" aria-labelledby="cta-section-title">
  <div class="wrap">
    <div class="eyebrow" style="justify-content:center; display:flex;" id="cta-section-tag">Teklif / Keşif</div>
    <h2 id="cta-section-title">Projenizi konuşalım.</h2>
    <div class="cta-actions">
      <a href="{WA}" class="btn btn-primary" target="_blank" rel="noopener">WhatsApp</a>
      <a href="tel:{PHONE_TEL}" class="btn btn-ghost">Ara</a>
    </div>
  </div>
</section>
"""

NAV = """  <nav aria-label="Ana menü">
    <a href="#teklif">Teklif</a>
    <a href="#iletisim">İletişim</a>
  </nav>"""

FOOTER_COLS = """      <div>
        <h4>Hizmetler</h4>
        <ul>
          <li><a href="/hizmetler/">Tüm hizmetler</a></li>
          <li><a href="/hizmetler/tabela/">Tabela</a></li>
          <li><a href="/hizmetler/isikli-tabela/">Işıklı Tabela</a></li>
          <li><a href="/hizmetler/kutu-harf/">Kutu Harf</a></li>
          <li><a href="/hizmetler/totem/">Totem</a></li>
          <li><a href="/hizmetler/cam-giydirme/">Cam Giydirme</a></li>
          <li><a href="/hizmetler/arac-giydirme/">Araç Giydirme</a></li>
          <li><a href="/hizmetler/lightbox/">Lightbox</a></li>
        </ul>
      </div>
      <div>
        <h4>Keşfet</h4>
        <ul>
          <li><a href="/projeler/">Projeler</a></li>
          <li><a href="/sektorler/">Sektörler</a></li>
          <li><a href="/bilgi/">Bilgi</a></li>
          <li><a href="#surec">Süreç</a></li>
          <li><a href="/bolgeler/tekirdag/">Tekirdağ</a></li>
          <li><a href="#teklif">Teklif Al</a></li>
        </ul>
      </div>
      <div>
        <h4>İletişim</h4>
        <ul>
          <li id="contact-email">merhaba@maltstudio.com</li>
          <li><a id="contact-phone" href="tel:+905525826959">05525826959</a></li>
          <li id="contact-address">Tekirdağ, Türkiye</li>
          <!-- Temporarily hidden; keep markup for easy re-enable -->
          <li hidden><a href="https://www.instagram.com/maltstudio.co/" id="social-instagram">Instagram</a></li>
          <li><a href="#teklif">Mesaj / Teklif</a></li>
        </ul>
      </div>"""


def inject_css(doc: str) -> str:
    marker = "  @media (max-width:900px){\n    nav{display:none;}"
    if marker not in doc:
        raise SystemExit("build_home_a3: CSS marker not found")
    # Drop prior A3 block if re-running
    doc = re.sub(
        r"\n  /\* -------- A3 home authority -------- \*/.*?(?=\n  @media \(max-width:900px\)\{\n    nav\{display:none;\})",
        "",
        doc,
        count=1,
        flags=re.S,
    )
    return doc.replace(marker, A3_CSS.rstrip() + "\n\n" + marker, 1)


def replace_nav(doc: str) -> str:
    return re.sub(r"<nav\b[^>]*>.*?</nav>", NAV.strip(), doc, count=1, flags=re.S)


def replace_main(doc: str) -> str:
    # From first hero section through CTA (before footer)
    pattern = re.compile(
        r'<section class="hero".*?<section class="cta"[^>]*>.*?</section>',
        re.S,
    )
    if not pattern.search(doc):
        # fallback: hero to footer
        pattern = re.compile(r'<section class="hero".*?(?=<footer>)', re.S)
        m = pattern.search(doc)
        if not m:
            raise SystemExit("build_home_a3: hero/main block not found")
        return doc[: m.start()] + MAIN.strip() + "\n\n" + doc[m.end() :]
    return pattern.sub(MAIN.strip(), doc, count=1)


def replace_footer_cols(doc: str) -> str:
    # Replace the three columns after brand column
    pattern = re.compile(
        r'(<div>\s*<h4>Hizmetler</h4>.*?</div>\s*)'
        r'(<div>\s*<h4>(?:Tekirdağ|Keşfet)</h4>.*?</div>\s*)'
        r'(<div>\s*<h4>İletişim</h4>.*?</div>)',
        re.S,
    )
    if not pattern.search(doc):
        print("warn: footer columns pattern not found; skipping footer enrich")
        return doc
    return pattern.sub(FOOTER_COLS, doc, count=1)


def fix_whatsapp_btn(doc: str) -> str:
    return re.sub(
        r'(id="whatsapp-btn"[^>]*href=")[^"]*"',
        rf'\1{WA_API}"',
        doc,
        count=1,
    )


def remove_kesfet_if_any(doc: str) -> str:
    return re.sub(
        r'\s*<section[^>]*id="kesfet"[^>]*>.*?</section>\s*',
        "\n",
        doc,
        count=1,
        flags=re.S,
    )


def sync_trust_tokens(doc: str) -> str:
    """Keep homepage inlined tokens in sync with site.css trust contrast."""
    doc = re.sub(
        r"(--trust-wash:\s*)rgba\(0,0,0,0\.(?:25|42)\)",
        r"\1rgba(0,0,0,0.42)",
        doc,
        count=1,
    )
    doc = re.sub(
        r"(--trust-wash:\s*)rgba\(26,26,26,0\.0[58]\)",
        r"\1rgba(26,26,26,0.08)",
        doc,
        count=1,
    )
    return doc


def main() -> int:
    doc = INDEX.read_text(encoding="utf-8")
    doc = inject_css(doc)
    doc = sync_trust_tokens(doc)
    doc = replace_nav(doc)
    doc = remove_kesfet_if_any(doc)
    doc = replace_main(doc)
    doc = replace_footer_cols(doc)
    doc = fix_whatsapp_btn(doc)
    # Ensure single iletisim alias for old anchors
    if 'id="iletisim"' not in doc:
        doc = doc.replace('id="teklif"', 'id="teklif" name="iletisim"', 1)
        # better: add hidden alias anchor
        doc = doc.replace(
            '<section class="cta" id="teklif"',
            '<div id="iletisim" hidden></div>\n<section class="cta" id="teklif"',
            1,
        )
    INDEX.write_text(doc, encoding="utf-8")
    print("build_home_a3: wrote index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
