#!/usr/bin/env python3
"""Self-check for the SEO collector. Exit 1 on failure. Does not mutate the site."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import collect as c  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def test_corpus() -> None:
    urls = c.load_urls()
    assert len(urls) == 35, len(urls)
    assert urls[0] == "https://maltstudio.co/"
    assert "https://maltstudio.co/hizmetler/tabela/" in urls
    assert "https://maltstudio.co/admin/" not in urls
    assert all(u.startswith("https://maltstudio.co/") for u in urls)


def test_paths() -> None:
    assert c.url_to_html("https://maltstudio.co/").is_file()
    assert c.url_to_html("https://maltstudio.co/hizmetler/tabela/").is_file()
    assert c.url_to_html("https://maltstudio.co/bilgi/tabela-cesitleri/").is_file()


def test_homepage_ld() -> None:
    rec = c.parse_page("https://maltstudio.co/")
    assert rec["status"] == 200
    assert rec["title"]
    assert rec["jsonld_parse_ok"] is True
    assert "LocalBusiness" in rec["schema_types"]
    assert rec["schema"]["has_website_node"] is True
    assert rec["h1_count"] == 1
    assert rec["schema"]["has_geo"] is True
    assert rec["schema"]["has_hours"] is True
    assert rec["schema"]["has_faqpage"] is True


def test_inner_ld_and_guides() -> None:
    tabela = c.parse_page("https://maltstudio.co/hizmetler/tabela/")
    assert tabela["jsonld_parse_ok"]
    assert "Service" in tabela["schema_types"]
    assert tabela["schema"]["ispartof_website"] is True
    assert "https://maltstudio.co/#website" not in tabela["schema"]["dangling_refs"]
    guide = c.parse_page("https://maltstudio.co/bilgi/tabela-cesitleri/")
    assert "Article" in guide["schema_types"]
    assert "WebPage" in guide["schema_types"]


def test_sitemap_invariants() -> None:
    sm = c.parse_sitemap()
    locs = sm["locs"]
    assert len(locs) == len(set(locs))
    assert all(u.startswith("https://maltstudio.co/") for u in locs)
    assert not sm.get("private_locs")
    assert "https://maltstudio.co/" in locs
    assert "https://maltstudio.co/gizlilik/" in locs
    assert "https://maltstudio.co/hakkimizda/" in locs
    assert "https://maltstudio.co/hizmetler/tabela/" in locs
    assert all("/admin/" not in u and "/proje/" not in u for u in locs)
    assert all("404" not in u for u in locs)


def test_frozen_files() -> None:
    q = json.loads((ROOT / "seo/benchmark/geo-queries.json").read_text(encoding="utf-8"))
    assert q["frozen"] is True
    for g in (
        "branded_informational",
        "branded_transactional",
        "non_branded_informational",
        "definition",
        "problem_solution",
        "recommendation",
        "comparison",
        "local_tekirdag",
    ):
        assert q["groups"][g]
    rubric = (ROOT / "seo/benchmark/geo-rubric.md").read_text(encoding="utf-8")
    assert "Entity clarity" in rubric
    assert "Extractability" in rubric


def main() -> None:
    test_corpus()
    test_paths()
    test_homepage_ld()
    test_inner_ld_and_guides()
    test_sitemap_invariants()
    test_frozen_files()
    print("seo collector self-check ok")


if __name__ == "__main__":
    main()
