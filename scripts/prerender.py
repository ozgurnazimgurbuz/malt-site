#!/usr/bin/env python3
"""Bake content.json into index.html for crawlable, CLS-free first paint.

Decap CMS continues to edit content.json. Netlify runs this on every deploy so
published HTML always matches the latest CMS commit. No npm dependencies.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content.json"
INDEX = ROOT / "index.html"


def esc(value) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def eyebrow_html(raw) -> str:
    """Keep CMS as one string; wrap leading 'Brand · ' so CSS can hide it everywhere."""
    text = "" if raw is None else str(raw)
    sep = " · "
    if sep in text:
        brand, rest = text.split(sep, 1)
        return f'<span class="eyebrow-brand">{esc(brand)}{sep}</span>{esc(rest)}'
    return esc(text)


def replace_inner_by_id(doc: str, element_id: str, inner: str) -> str:
    """Replace innerHTML of first element with id=element_id (nested-safe)."""
    open_re = re.compile(
        rf'<([a-zA-Z][\w-]*)([^>]*\sid="{re.escape(element_id)}"[^>]*)>',
        re.S,
    )
    match = open_re.search(doc)
    if not match:
        raise SystemExit(f'prerender: element id="{element_id}" not found')
    tag = match.group(1)
    start_inner = match.end()
    i = start_inner
    depth = 1
    tag_re = re.compile(rf'</?{re.escape(tag)}\b[^>]*>', re.I)
    while depth and i < len(doc):
        m = tag_re.search(doc, i)
        if not m:
            raise SystemExit(f'prerender: unclosed id="{element_id}"')
        token = m.group(0)
        if token.startswith("</"):
            depth -= 1
            if depth == 0:
                return doc[:start_inner] + inner + doc[m.start() :]
        elif token.endswith("/>"):
            pass
        else:
            depth += 1
        i = m.end()
    raise SystemExit(f'prerender: unclosed id="{element_id}"')


def set_attr_by_id(doc: str, element_id: str, attr: str, value: str) -> str:
    pattern = re.compile(
        rf'<([a-zA-Z][\w-]*)([^>]*\sid="{re.escape(element_id)}"[^>]*)>',
        re.S,
    )
    match = pattern.search(doc)
    if not match:
        raise SystemExit(f'prerender: element id="{element_id}" not found for attr')
    tag_name, attrs = match.group(1), match.group(2)
    attr_pat = re.compile(rf'\s{re.escape(attr)}="[^"]*"')
    attrs = attr_pat.sub("", attrs)
    attrs = f'{attrs} {attr}="{esc(value)}"'
    return doc[: match.start()] + f"<{tag_name}{attrs}>" + doc[match.end() :]


def abs_url(site_url: str, path: str) -> str:
    site = (site_url or "").rstrip("/")
    if not site or not path:
        return ""
    return site + (path if path.startswith("/") else "/" + path)


def to_e164(phone: str, wa: str) -> str:
    from_wa = re.sub(r"\D", "", wa or "")
    if re.fullmatch(r"90\d{10}", from_wa):
        return "+" + from_wa
    digits = re.sub(r"\D", "", phone or "")
    if re.fullmatch(r"90\d{10}", digits):
        return "+" + digits
    if re.fullmatch(r"0\d{10}", digits):
        return "+90" + digits[1:]
    if re.fullmatch(r"\d{10}", digits):
        return "+90" + digits
    return ""


def is_profile_url(raw: str) -> bool:
    try:
        from urllib.parse import urlparse

        u = urlparse(raw)
        if u.scheme != "https":
            return False
        host = u.hostname.replace("www.", "") if u.hostname else ""
        path = (u.path or "/").rstrip("/") or "/"
        bare = {
            "linkedin.com",
            "behance.net",
            "youtube.com",
            "youtu.be",
            "instagram.com",
            "facebook.com",
            "x.com",
            "twitter.com",
            "tiktok.com",
        }
        if host in bare and path == "/":
            return False
        return len(path) > 1
    except Exception:
        return False


def prune(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            pv = prune(v)
            if pv in ("", None, [], {}):
                continue
            out[k] = pv
        return out
    if isinstance(obj, list):
        return [prune(x) for x in obj if prune(x) not in ("", None, [], {})]
    return obj


def build_services(c: dict) -> str:
    cards = []
    for i, s in enumerate(c.get("services") or []):
        title = esc(s.get("title"))
        desc = esc(s.get("description"))
        num = f"{i + 1:02d}"
        href = (s.get("href") or "").strip()
        inner = (
            f'<div class="service-num">{num}</div>'
            f"<h3>{title}</h3>"
            f"<p>{desc}</p>"
        )
        if href:
            cards.append(
                f'<a class="service-card" href="{esc(href)}">{inner}</a>'
            )
        else:
            cards.append(f'<div class="service-card">{inner}</div>')
    return "".join(cards)


def portfolio_image_markup(image: str, alt: str, *, lazy: bool = True) -> str:
    """Card image with WebP sibling when present (optimize_uploads.py)."""
    src = esc(image)
    webp = ""
    lower = image.lower()
    for ext in (".jpeg", ".jpg", ".png"):
        if lower.endswith(ext):
            candidate = image[: -len(ext)] + ".webp"
            if (ROOT / candidate.lstrip("/")).is_file():
                webp = esc(candidate)
            break
    sizes = "(max-width:560px) 100vw, (max-width:900px) 50vw, 33vw"
    loading = ' loading="lazy"' if lazy else ""
    prio = ' fetchpriority="high"' if not lazy else ""
    decoding = ' decoding="async"' if lazy else ""
    img = (
        f'<img class="work-swatch" src="{src}" alt="{alt}" '
        f'width="800" height="1000" sizes="{sizes}"'
        f"{loading}{prio}{decoding}>"
    )
    if webp:
        return (
            f"<picture>"
            f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f"{img}"
            f"</picture>"
        )
    return img


def build_portfolio(c: dict) -> str:
    items = []
    for p in c.get("portfolio") or []:
        name = esc(p.get("name"))
        category = esc(p.get("category"))
        desc = p.get("description") or ""
        image = p.get("image") or ""
        slug = (p.get("slug") or "").strip().strip("/")
        cat_attr = f' data-cat="{category}"' if category else ""
        if image:
            alt = esc(f'{p.get("name") or ""} uygulama projesi')
            swatch = portfolio_image_markup(image, alt, lazy=len(items) > 0)
        else:
            color1 = esc(p.get("color1") or "#B08D72")
            color2 = esc(p.get("color2") or "#1a1a1a")
            swatch = (
                f'<div class="work-swatch" '
                f'style="background:linear-gradient(135deg, {color1}, {color2})"></div>'
            )
        meta = f'<div class="work-meta"><div class="work-name">{name}</div>'
        if desc:
            meta += f'<div class="work-desc">{esc(desc)}</div>'
        meta += "</div>"
        inner = f"{swatch}{meta}"
        if slug:
            href = f"/projeler/{esc(slug)}/"
            items.append(
                f'<a class="work-item" href="{href}"{cat_attr}>{inner}</a>'
            )
        else:
            items.append(f'<div class="work-item"{cat_attr}>{inner}</div>')
    return "".join(items)


def build_stats(c: dict) -> str:
    cells = []
    for s in c.get("stats") or []:
        cells.append(
            f"<div>"
            f'<div class="stat-num">{esc(s.get("number"))}</div>'
            f'<div class="stat-label">{esc(s.get("label"))}</div>'
            f"</div>"
        )
    return "".join(cells)


def services_title_html(title: str) -> str:
    title = title or ""
    if title.count(" ") == 1:
        cut = title.find(" ")
        return esc(title[:cut]) + "<br> " + esc(title[cut + 1 :])
    return esc(title)


def hero_title_html(c: dict) -> str:
    h1 = (c.get("heroH1") or "").strip()
    if h1:
        return esc(h1)
    top = esc(c.get("heroTitleTop"))
    highlight = esc(c.get("heroHighlight"))
    bottom = esc(c.get("heroTitleBottom"))
    return (
        f'{top} <span id="hero-highlight">{highlight}</span>'
        f'<br id="hero-br">{bottom}'
    )


def replace_hero_title(doc: str, c: dict) -> str:
    """Replace entire H1 — nested spans break replace_inner_by_id."""
    pattern = re.compile(
        r'<h1\s+id="hero-title"[^>]*>.*?</h1>',
        re.S | re.I,
    )
    if not pattern.search(doc):
        raise SystemExit('prerender: <h1 id="hero-title"> not found')
    return pattern.sub(
        f'<h1 id="hero-title">{hero_title_html(c)}</h1>',
        doc,
        count=1,
    )


def extract_faq_pairs(html: str, scope_class: str = "home-faq") -> list[tuple[str, str]]:
    block_m = re.search(
        rf'<div class="{re.escape(scope_class)}"[^>]*>(.*?)</div>',
        html,
        re.I | re.S,
    )
    chunk = block_m.group(1) if block_m else html
    return [
        (m.group(1).strip(), m.group(2).strip())
        for m in re.finditer(
            r"<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>",
            chunk,
            re.I | re.S,
        )
    ]


def _knows_about(c: dict) -> list[str]:
    names: list[str] = []
    for s in c.get("services") or []:
        t = (s.get("title") or "").strip() if isinstance(s, dict) else str(s).strip()
        if t and t not in names:
            names.append(t)
    return names


def _opening_hours(c: dict) -> list[dict]:
    out = []
    for h in c.get("openingHours") or []:
        if not isinstance(h, dict):
            continue
        days = [d for d in re.split(r"[,\s]+", str(h.get("days") or "")) if d]
        if days and h.get("opens") and h.get("closes"):
            out.append(
                {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": days,
                    "opens": h["opens"],
                    "closes": h["closes"],
                }
            )
    return out


def build_json_ld(c: dict, faqs: list[tuple[str, str]] | None = None) -> dict:
    """Authoritative homepage graph. One LocalBusiness @id; no client-JS duplicate."""
    site = (c.get("siteUrl") or "").rstrip("/")
    if not site or not c.get("siteName"):
        return {}
    telephone = to_e164(c.get("phone", ""), c.get("whatsappNumber", ""))
    same_as = [
        u
        for u in (c.get("instagram"), c.get("linkedin"), c.get("youtube"), c.get("behance"))
        if u and is_profile_url(u)
    ]
    lat, lng = c.get("geoLatitude"), c.get("geoLongitude")
    geo = {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng} if lat and lng else None
    logo_url = abs_url(site, c.get("logo") or "/images/icon-512.png")
    description = c.get("seoDescription") or c.get("footerAbout") or ""
    maps = (c.get("googleMapsUrl") or "").strip()
    if maps and not maps.startswith("https://"):
        maps = ""
    biz = prune(
        {
            "@type": ["LocalBusiness", "ProfessionalService"],
            "@id": site + "/#business",
            "name": c.get("siteName"),
            "url": site + "/",
            "telephone": telephone,
            "email": c.get("email"),
            "description": description or None,
            "address": prune(
                {
                    "@type": "PostalAddress",
                    "streetAddress": c.get("addressStreet"),
                    "postalCode": c.get("addressPostalCode"),
                    "addressLocality": c.get("addressLocality"),
                    "addressRegion": c.get("addressRegion"),
                    "addressCountry": c.get("addressCountry") or "TR",
                }
            ),
            "geo": geo,
            "openingHoursSpecification": _opening_hours(c) or None,
            "logo": logo_url or None,
            "image": abs_url(site, c.get("seoOgImage") or "/images/og.jpg") or None,
            "hasMap": maps or None,
            "areaServed": [
                {"@type": "City", "name": "Tekirdağ"},
                {
                    "@type": "AdministrativeArea",
                    "name": c.get("addressLocality") or "Süleymanpaşa",
                },
            ],
            "knowsAbout": _knows_about(c) or None,
            "sameAs": same_as or None,
            "priceRange": c.get("priceRange") or None,
        }
    )
    website = prune(
        {
            "@type": "WebSite",
            "@id": site + "/#website",
            "url": site + "/",
            "name": c.get("siteName"),
            "description": description or None,
            "publisher": {"@id": site + "/#business"},
            "inLanguage": c.get("defaultLocale") or "tr-TR",
        }
    )
    webpage = prune(
        {
            "@type": "WebPage",
            "@id": site + "/#webpage",
            "url": site + "/",
            "name": c.get("seoTitle") or c.get("siteName"),
            "description": description or None,
            "isPartOf": {"@id": site + "/#website"},
            "about": {"@id": site + "/#business"},
            "inLanguage": c.get("defaultLocale") or "tr-TR",
        }
    )
    graph = [g for g in (biz, website, webpage) if g]
    if faqs:
        sys.path.insert(0, str(ROOT / "scripts"))
        from lib_site import faq_ld  # noqa: WPS433

        faq_node = faq_ld(site + "/", faqs)
        if faq_node and faq_node.get("mainEntity"):
            graph.append(faq_node)
    return {"@context": "https://schema.org", "@graph": graph}


def set_meta(doc: str, attr: str, key: str, content: str) -> str:
    if not content:
        return doc
    pattern = re.compile(
        rf'(<meta\s+{attr}="{re.escape(key)}"[^>]*content=")[^"]*(")',
        re.I,
    )
    if pattern.search(doc):
        return pattern.sub(rf"\g<1>{esc(content)}\2", doc, count=1)
    # insert before </head>
    tag = f'<meta {attr}="{key}" content="{esc(content)}">'
    return doc.replace("</head>", tag + "\n</head>", 1)


def set_title(doc: str, title: str) -> str:
    if not title:
        return doc
    return re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", doc, count=1, flags=re.S)


def replace_json_ld(doc: str, data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    block = f'<script type="application/ld+json" id="ld-json">{payload}</script>'
    if re.search(r'<script type="application/ld\+json" id="ld-json">', doc):
        return re.sub(
            r'<script type="application/ld\+json" id="ld-json">[\s\S]*?</script>',
            block,
            doc,
            count=1,
        )
    return doc.replace("</head>", block + "\n</head>", 1)


_GA_ID_RE = re.compile(r"^G-[A-Z0-9]+$")


def ensure_gtag(doc: str, ga_id: str) -> str:
    """Insert deferred GA4 once in <head>; strip prior Google tag blocks first."""
    # Import locally so prerender stays usable without full package layout.
    sys.path.insert(0, str(ROOT / "scripts"))
    from lib_site import gtag_snippet  # noqa: WPS433

    doc = re.sub(
        r"\s*<!--\s*Google tag \(gtag\.js\)[^>]*-->\s*"
        r'(?:<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-[A-Z0-9]+"></script>\s*)?'
        r"<script>\s*[\s\S]*?(?:gtag\('config'|__gaLoaded|googletagmanager)[\s\S]*?</script>",
        "",
        doc,
        count=1,
        flags=re.I,
    )
    doc = re.sub(
        r'\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-[A-Z0-9]+"></script>\s*'
        r"<script>\s*window\.dataLayer[\s\S]*?gtag\('config',\s*'G-[A-Z0-9]+'\);[\s\S]*?</script>",
        "",
        doc,
        count=1,
        flags=re.I,
    )
    ga_id = (ga_id or "").strip()
    if not _GA_ID_RE.match(ga_id):
        return doc
    block = gtag_snippet(ga_id)
    if not block:
        return doc
    # Prefer after theme boot (if present), else after viewport, else before </head>.
    boot = re.search(
        r"<script>\(function\(\)\{try\{if\(localStorage\.getItem\('malt-theme'\)[\s\S]*?</script>\s*",
        doc,
    )
    if boot:
        return doc[: boot.end()] + block + doc[boot.end() :]
    vp = re.search(r'<meta name="viewport"[^>]*>\s*', doc, flags=re.I)
    if vp:
        return doc[: vp.end()] + block + doc[vp.end() :]
    return doc.replace("</head>", block + "</head>", 1)




def main() -> int:
    c = json.loads(CONTENT.read_text(encoding="utf-8"))
    doc = INDEX.read_text(encoding="utf-8")

    # Mark body as prerendered so client JS skips duplicate grid work.
    if 'data-prerendered=' not in doc:
        doc = doc.replace("<body>", '<body data-prerendered="1">', 1)
    else:
        doc = re.sub(r"<body[^>]*>", '<body data-prerendered="1">', doc, count=1)

    doc = replace_inner_by_id(doc, "hero-eyebrow", eyebrow_html(c.get("eyebrow")))
    doc = replace_hero_title(doc, c)
    doc = replace_inner_by_id(doc, "hero-sub", esc(c.get("heroSub")))
    doc = replace_inner_by_id(doc, "cta-primary", esc(c.get("ctaPrimary") or "Teklif Al"))
    doc = replace_inner_by_id(doc, "cta-secondary", esc(c.get("ctaSecondary") or "WhatsApp"))
    # Hero CTAs: Teklif → on-page anchor; WhatsApp → wa link (no new URLs)
    doc = set_attr_by_id(doc, "cta-primary", "href", "#teklif")
    if c.get("whatsappNumber"):
        from urllib.parse import quote

        msg = quote(c.get("whatsappMessage") or "Merhaba, teklif almak istiyorum.")
        wa = f"https://wa.me/{c['whatsappNumber']}?text={msg}"
        doc = set_attr_by_id(doc, "cta-secondary", "href", wa)
        doc = set_attr_by_id(doc, "cta-secondary", "target", "_blank")
        doc = set_attr_by_id(doc, "cta-secondary", "rel", "noopener")

    doc = replace_inner_by_id(doc, "services-tag", esc(c.get("servicesTag")))
    doc = replace_inner_by_id(doc, "services-title", services_title_html(c.get("servicesTitle") or ""))
    doc = replace_inner_by_id(doc, "services-intro", esc(c.get("servicesIntro")))
    doc = replace_inner_by_id(doc, "service-grid", build_services(c))

    doc = replace_inner_by_id(doc, "portfolio-tag", esc(c.get("portfolioTag")))
    doc = replace_inner_by_id(doc, "portfolio-title", esc(c.get("portfolioTitle")))
    doc = replace_inner_by_id(doc, "portfolio-intro", esc(c.get("portfolioIntro")))
    doc = replace_inner_by_id(doc, "work-grid", build_portfolio(c))

    doc = replace_inner_by_id(doc, "stats-grid", build_stats(c))

    doc = replace_inner_by_id(doc, "cta-section-tag", esc(c.get("ctaSectionTag")))
    # Keep intentional line break in CTA title if present in HTML; prefer CMS plain text.
    cta_title = c.get("ctaSectionTitle") or ""
    doc = replace_inner_by_id(doc, "cta-section-title", esc(cta_title))

    doc = replace_inner_by_id(doc, "footer-about", esc(c.get("footerAbout")))
    doc = replace_inner_by_id(doc, "contact-email", esc(c.get("email")))
    phone_display = c.get("phoneDisplay") or "+90 552 582 69 59"
    doc = replace_inner_by_id(doc, "contact-phone", esc(phone_display))
    doc = replace_inner_by_id(doc, "contact-address", esc(c.get("address")))
    doc = replace_inner_by_id(doc, "copyright-text", esc(c.get("copyrightText")))

    if c.get("instagram"):
        doc = set_attr_by_id(doc, "social-instagram", "href", c["instagram"])
    if c.get("linkedin"):
        doc = set_attr_by_id(doc, "social-linkedin", "href", c["linkedin"])
    if c.get("behance"):
        doc = set_attr_by_id(doc, "social-behance", "href", c["behance"])
    if c.get("youtube"):
        doc = set_attr_by_id(doc, "social-youtube", "href", c["youtube"])

    if c.get("whatsappNumber"):
        from urllib.parse import quote

        msg = quote(c.get("whatsappMessage") or "")
        wa = f"https://api.whatsapp.com/send?phone={c['whatsappNumber']}&text={msg}"
        doc = set_attr_by_id(doc, "whatsapp-btn", "href", wa)

    # Head SEO
    doc = set_title(doc, c.get("seoTitle") or "")
    doc = set_meta(doc, "name", "description", c.get("seoDescription") or "")
    doc = set_meta(doc, "name", "keywords", c.get("seoKeywords") or "")
    # Token lives in content.json googleSearchConsoleVerification. Empty → no tag.
    gsc = (c.get("googleSearchConsoleVerification") or "").strip()
    if gsc:
        doc = set_meta(doc, "name", "google-site-verification", gsc)
    doc = set_meta(doc, "property", "og:title", c.get("seoTitle") or "")
    doc = set_meta(doc, "property", "og:description", c.get("seoDescription") or "")
    doc = set_meta(doc, "property", "og:url", c.get("canonicalUrl") or "")
    doc = set_meta(doc, "property", "og:site_name", c.get("siteName") or "")
    og = abs_url(c.get("siteUrl") or "", c.get("seoOgImage") or "")
    if og:
        doc = set_meta(doc, "property", "og:image", og)
        doc = set_meta(doc, "property", "og:image:secure_url", og)
        doc = set_meta(doc, "name", "twitter:image", og)
    doc = set_meta(doc, "name", "twitter:title", c.get("seoTitle") or "")
    doc = set_meta(doc, "name", "twitter:description", c.get("seoDescription") or "")
    og_alt = c.get("seoTitle") or c.get("siteName") or ""
    if og_alt:
        doc = set_meta(doc, "property", "og:image:alt", og_alt)
        doc = set_meta(doc, "name", "twitter:image:alt", og_alt)

    doc = ensure_gtag(doc, c.get("googleAnalyticsId") or "")

    faqs = extract_faq_pairs(doc)
    ld = build_json_ld(c, faqs=faqs)
    if ld:
        doc = replace_json_ld(doc, ld)

    INDEX.write_text(doc, encoding="utf-8")
    print(f"prerender: wrote {INDEX.relative_to(ROOT)} from {CONTENT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
