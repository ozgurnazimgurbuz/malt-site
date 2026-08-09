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
    """Keep CMS as one string; wrap leading 'Brand · ' for mobile CSS hide."""
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
    pattern = re.compile(rf'(id="{re.escape(element_id)}"[^>]*)>', re.S)
    match = pattern.search(doc)
    if not match:
        raise SystemExit(f'prerender: element id="{element_id}" not found for attr')
    tag = match.group(1)
    attr_pat = re.compile(rf'\s{attr}="[^"]*"')
    if attr_pat.search(tag):
        tag = attr_pat.sub(f' {attr}="{esc(value)}"', tag)
    else:
        tag = f'{tag} {attr}="{esc(value)}"'
    return doc[: match.start(1)] + tag + doc[match.end(1) :]


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


def portfolio_image_markup(image: str, alt: str) -> str:
    """Card image with WebP sibling when present (optimize_uploads.py).

    sizes matches .work-grid breakpoints in index.html (1 / 2 / 3 columns).
    width/height keep 4:5 aspect for CLS; CSS object-fit:cover crops.
    """
    src = esc(image)
    webp = ""
    lower = image.lower()
    for ext in (".jpeg", ".jpg", ".png"):
        if lower.endswith(ext):
            candidate = image[: -len(ext)] + ".webp"
            if (ROOT / candidate.lstrip("/")).is_file():
                webp = esc(candidate)
            break
    # ~full width mobile, half tablet, third desktop — 1200w source covers 2x.
    sizes = "(max-width:560px) 100vw, (max-width:900px) 50vw, 33vw"
    img = (
        f'<img class="work-swatch" src="{src}" alt="{alt}" '
        f'width="800" height="1000" sizes="{sizes}" '
        f'loading="lazy" decoding="async">'
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
            alt = esc(f'{p.get("name") or ""} - {p.get("category") or ""}')
            swatch = portfolio_image_markup(image, alt)
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
    cut = title.find(" ")
    if cut == -1:
        return esc(title)
    return esc(title[:cut]) + "<br>" + esc(title[cut + 1 :])


def hero_title_html(c: dict) -> str:
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


def build_json_ld(c: dict) -> dict:
    site = (c.get("siteUrl") or "").rstrip("/")
    if not site or not c.get("siteName"):
        return {}
    telephone = to_e164(c.get("phone", ""), c.get("whatsappNumber", ""))
    description = c.get("seoDescription") or c.get("footerAbout") or ""
    page_url = c.get("canonicalUrl") or (site + "/")
    logo_url = abs_url(site, c.get("logo") or "/images/icon-512.png")
    og_url = abs_url(site, c.get("seoOgImage") or "")
    image_url = og_url or logo_url
    same_as = [
        u
        for u in [c.get("instagram"), c.get("linkedin"), c.get("behance"), c.get("youtube")]
        if u and is_profile_url(u)
    ]
    schema_services = []
    for s in c.get("schemaServices") or []:
        schema_services.append(s if isinstance(s, str) else (s or {}).get("service"))
    schema_services = [s for s in schema_services if s]
    page_services = [s.get("title") for s in (c.get("services") or []) if s.get("title")]
    service_names = list(dict.fromkeys([*schema_services, *page_services]))

    postal = prune(
        {
            "@type": "PostalAddress",
            "streetAddress": c.get("addressStreet"),
            "addressLocality": c.get("addressLocality")
            or ((c.get("address") or "").split(",")[0].strip() or None),
            "addressRegion": c.get("addressRegion"),
            "postalCode": c.get("addressPostalCode"),
            "addressCountry": c.get("addressCountry") or "TR",
        }
    )
    geo = None
    if c.get("geoLatitude") and c.get("geoLongitude"):
        geo = prune(
            {
                "@type": "GeoCoordinates",
                "latitude": c.get("geoLatitude"),
                "longitude": c.get("geoLongitude"),
            }
        )
    opening = []
    for h in c.get("openingHours") or []:
        days = [d for d in re.split(r"[,\s]+", h.get("days") or "") if d]
        item = prune(
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": days,
                "opens": h.get("opens"),
                "closes": h.get("closes"),
            }
        )
        if item.get("dayOfWeek") and item.get("opens") and item.get("closes"):
            opening.append(item)

    logo_obj = prune(
        {
            "@type": "ImageObject",
            "@id": site + "/#logo",
            "url": logo_url,
            "contentUrl": logo_url,
            "width": None if c.get("logo") else 512,
            "height": None if c.get("logo") else 512,
            "caption": c.get("siteName") + " logo",
        }
    )
    primary = prune(
        {
            "@type": "ImageObject",
            "@id": site + "/#primaryimage",
            "url": image_url,
            "contentUrl": image_url,
            "width": 1200 if og_url else None,
            "height": 630 if og_url else None,
            "caption": c.get("seoTitle") or c.get("siteName"),
        }
    )
    contact = prune(
        {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "email": c.get("email"),
            "telephone": telephone,
            "areaServed": "TR",
            "availableLanguage": ["Turkish", "tr"],
        }
    )
    area = [
        prune(
            {
                "@type": "AdministrativeArea",
                "name": c.get("addressLocality") or "Tekirdağ",
            }
        ),
        prune(
            {
                "@type": "Country",
                "name": "Türkiye",
                "sameAs": "https://www.wikidata.org/wiki/Q43",
            }
        ),
    ]
    catalog = None
    if service_names:
        catalog = {
            "@type": "OfferCatalog",
            "name": "Hizmetler",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": i,
                    "item": prune(
                        {
                            "@type": "Offer",
                            "itemOffered": prune(
                                {
                                    "@type": "Service",
                                    "name": name,
                                    "provider": {"@id": site + "/#localbusiness"},
                                }
                            ),
                        }
                    ),
                }
                for i, name in enumerate(service_names, 1)
            ],
        }

    org = prune(
        {
            "@type": "Organization",
            "@id": site + "/#organization",
            "name": c.get("siteName"),
            "legalName": c.get("legalName"),
            "brand": prune({"@type": "Brand", "name": c.get("siteName")}),
            "url": site + "/",
            "logo": {"@id": site + "/#logo"} if logo_obj else None,
            "image": {"@id": site + "/#primaryimage"} if primary else None,
            "description": description,
            "foundingDate": c.get("foundingDate"),
            "email": c.get("email"),
            "telephone": telephone,
            "sameAs": same_as,
            "areaServed": area,
            "knowsAbout": service_names,
            "contactPoint": contact,
        }
    )
    biz = prune(
        {
            "@type": ["LocalBusiness", "ProfessionalService"],
            "@id": site + "/#localbusiness",
            "name": c.get("siteName"),
            "legalName": c.get("legalName"),
            "url": site + "/",
            "parentOrganization": {"@id": site + "/#organization"},
            "image": {"@id": site + "/#primaryimage"} if primary else None,
            "logo": {"@id": site + "/#logo"} if logo_obj else None,
            "description": description,
            "email": c.get("email"),
            "telephone": telephone,
            "address": postal,
            "geo": geo,
            "hasMap": c.get("googleMapsUrl"),
            "openingHoursSpecification": opening,
            "priceRange": c.get("priceRange"),
            "contactPoint": contact,
            "sameAs": same_as,
            "areaServed": area,
            "knowsAbout": service_names,
            "hasOfferCatalog": catalog,
            "foundingDate": c.get("foundingDate"),
        }
    )
    website = prune(
        {
            "@type": "WebSite",
            "@id": site + "/#website",
            "url": site + "/",
            "name": c.get("siteName"),
            "description": description,
            "publisher": {"@id": site + "/#organization"},
            "inLanguage": c.get("defaultLocale") or "tr-TR",
        }
    )
    webpage = prune(
        {
            "@type": "WebPage",
            "@id": site + "/#webpage",
            "url": page_url,
            "name": c.get("seoTitle") or c.get("siteName"),
            "description": description,
            "isPartOf": {"@id": site + "/#website"},
            "about": {"@id": site + "/#localbusiness"},
            "primaryImageOfPage": {"@id": site + "/#primaryimage"} if primary else None,
            "inLanguage": c.get("defaultLocale") or "tr-TR",
        }
    )
    graph = [org, biz, website, webpage]
    if logo_obj:
        graph.append(logo_obj)
    if primary:
        graph.append(primary)
    return {"@context": "https://schema.org", "@graph": [g for g in graph if g]}


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
    doc = replace_inner_by_id(doc, "contact-phone", esc(c.get("phone")))
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

    doc = ensure_gtag(doc, c.get("googleAnalyticsId") or "")

    ld = build_json_ld(c)
    if ld:
        doc = replace_json_ld(doc, ld)

    INDEX.write_text(doc, encoding="utf-8")
    print(f"prerender: wrote {INDEX.relative_to(ROOT)} from {CONTENT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
