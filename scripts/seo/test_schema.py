#!/usr/bin/env python3
"""SCHEMA-001/002: prerender JSON-LD must ship a coherent homepage graph. Fail if thin."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import prerender as p  # noqa: E402
from lib_site import faq_ld, visible_text  # noqa: E402

CMS = json.loads((Path(__file__).resolve().parents[2] / "content.json").read_text(encoding="utf-8"))


def test_homepage_graph_has_website_geo_hours() -> None:
    graph = p.build_json_ld(CMS)
    nodes = graph["@graph"]
    ids = {n.get("@id"): n for n in nodes if n.get("@id")}
    site = CMS["siteUrl"].rstrip("/")
    biz = ids[site + "/#business"]
    web = ids[site + "/#website"]
    page = ids[site + "/#webpage"]
    assert "LocalBusiness" in biz["@type"]
    assert "ProfessionalService" in biz["@type"]
    assert biz["geo"]["latitude"] == CMS["geoLatitude"]
    assert biz["geo"]["longitude"] == CMS["geoLongitude"]
    assert biz["openingHoursSpecification"]
    assert biz["openingHoursSpecification"][0]["opens"] == "09:00"
    assert biz["logo"]
    assert len(biz["knowsAbout"]) >= 3
    assert web["publisher"]["@id"] == site + "/#business"
    assert page["isPartOf"]["@id"] == site + "/#website"
    assert page["about"]["@id"] == site + "/#business"
    biz_nodes = [
        n
        for n in nodes
        if "LocalBusiness" in (n.get("@type") if isinstance(n.get("@type"), list) else [n.get("@type")])
    ]
    assert len(biz_nodes) == 1
    assert web["publisher"]["@id"] == site + "/#business"
    assert page["isPartOf"]["@id"] == site + "/#website"
    assert page["about"]["@id"] == site + "/#business"
    same = biz.get("sameAs") or []
    assert "linkedin.com/company/malt-studio" not in same
    assert any("instagram.com/maltstudio.co" in str(u) for u in same)
    # hasMap is the CMS maps URL (coordinate search), not a fabricated Place ID
    if CMS.get("googleMapsUrl"):
        assert biz.get("hasMap") == CMS["googleMapsUrl"]


def test_faq_ld_matches_visible_html() -> None:
    faqs = [
        ("Keşif ücretli mi?", "Keşif randevusu WhatsApp veya telefon ile alınır."),
        ("Linkli?", 'Detay için <a href="/bolgeler/tekirdag/">atölye</a> sayfasına bakın.'),
    ]
    node = faq_ld("https://maltstudio.co/", faqs)
    assert node["@type"] == "FAQPage"
    assert node["mainEntity"][0]["name"] == "Keşif ücretli mi?"
    assert node["mainEntity"][1]["acceptedAnswer"]["text"] == visible_text(faqs[1][1])
    assert "<a " not in node["mainEntity"][1]["acceptedAnswer"]["text"]


def test_no_linkedin_from_empty_cms() -> None:
    assert (CMS.get("linkedin") or "") == ""


def test_gsc_meta_omitted_when_empty() -> None:
    stub = "<html><head></head><body></html>"
    assert "google-site-verification" not in p.set_meta(
        stub, "name", "google-site-verification", ""
    )
    filled = p.set_meta(stub, "name", "google-site-verification", "token-from-gsc")
    assert 'name="google-site-verification"' in filled
    assert 'content="token-from-gsc"' in filled
    assert (CMS.get("googleSearchConsoleVerification") or "") == ""


def test_md_converter_spaces_service_card() -> None:
    import build_llms as llms

    html = (
        "<html><body><main>"
        '<a class="service-card" href="/hizmetler/tabela/">'
        '<div class="service-num">01</div><h3>Tabela</h3>'
        "<p>Dış ve iç mekan tabela üretimi ve montajı.</p>"
        "</a></main></body></html>"
    )
    md = llms.html_to_markdown(html, "https://maltstudio.co/")
    assert "01TabelaDış" not in md
    assert "###\n" not in md
    assert "[01 Tabela Dış ve iç mekan tabela üretimi ve montajı.]" in md
    assert "merhaba@maltstudio.co" in md
    assert "Yavuz Mahallesi" in md


def main() -> None:
    test_homepage_graph_has_website_geo_hours()
    test_faq_ld_matches_visible_html()
    test_no_linkedin_from_empty_cms()
    test_gsc_meta_omitted_when_empty()
    test_md_converter_spaces_service_card()
    print("schema self-check ok")


if __name__ == "__main__":
    main()
