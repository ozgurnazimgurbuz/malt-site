#!/usr/bin/env python3
"""Self-check for project tracking builder. Exit 1 on failure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_project_tracking as t  # noqa: E402

DEMO_SLUG = "mantra-garage-7f3k9x"


def _steps(*statuses: str) -> list[dict]:
    return [
        {"title": f"A{i+1}", "description": "", "status": s, "completedDate": ""}
        for i, s in enumerate(statuses)
    ]


def test_validation() -> None:
    # Happy: one current, matching currentStep
    steps, n = t.validate_and_resolve(_steps("completed", "completed", "current", "pending", "pending"), 3)
    assert n == 3 and steps[2]["status"] == "current"

    # Happy: derive from currentStep only
    steps, n = t.validate_and_resolve(_steps("pending", "pending", "pending"), 2)
    assert n == 2
    assert [s["status"] for s in steps] == ["completed", "current", "pending"]

    # Conflict: currentStep vs status
    try:
        t.validate_and_resolve(_steps("completed", "current", "pending"), 3, source="x.json")
        raise AssertionError("expected conflict")
    except t.TrackValidationError as e:
        assert "çelişiyor" in str(e)

    # Multiple current
    try:
        t.validate_and_resolve(_steps("current", "current"), None, source="x.json")
        raise AssertionError("expected multi-current")
    except t.TrackValidationError as e:
        assert "birden fazla" in str(e)

    # Neither source
    try:
        t.validate_and_resolve(_steps("pending", "pending"), None, source="x.json")
        raise AssertionError("expected missing current")
    except t.TrackValidationError as e:
        assert "currentStep boş" in str(e)


def test_demo_page() -> None:
    t.main()
    html = Path(t.OUT_DIR / DEMO_SLUG / "index.html").read_text(encoding="utf-8")
    assert "Mantra Garage" in html
    assert "Mantra Garage Tabela" not in html
    assert f"/proje/{DEMO_SLUG}/" in html
    assert "noindex, nofollow" in html
    assert "Üretimde" in html
    assert "Kutu harfler hazırlandı" in html
    assert "Kasa imalatta" in html
    assert "Kompozit derz sırasında" in html
    assert "track-notes" in html
    notes_at = html.find("track-notes")
    timeline_at = html.find("track-timeline")
    assert 0 <= notes_at < timeline_at
    assert "Kutu harfler hazırlandı" not in html[timeline_at:]
    assert "track-now-desc" not in html
    assert "Kutu harfler imalatta" not in html
    assert "Demir kasa imalatta" not in html
    assert "Kompozit derz sırası bekliyor" not in html
    assert "track-now-name" in html
    # Timeline keeps stage name "Üretim"; hero shows "Üretimde"
    assert 'track-step-title">Üretim</div>' in html
    assert "13 Ağustos 2026" in html
    assert "Son güncelleme" in html
    assert "wa.me" in html
    assert "tel:+905525826959" in html
    assert "Teklif Al" not in html
    assert html.count('data-status="completed"') == 2
    assert html.count('data-status="current"') == 1
    assert html.count('data-status="pending"') == 1
    assert "Teslim" not in html
    assert "22.500₺/45.000₺" in html
    assert "Kalan bakiye" in html
    assert not (t.OUT_DIR / "index.html").exists()
    assert not (t.OUT_DIR / "mantar-garage-7f3k9x").exists()
    assert "/proje/" not in Path(t.ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert "Disallow: /proje/" in Path(t.ROOT / "robots.txt").read_text(encoding="utf-8")
    cj = Path(t.ROOT / "content.json").read_text(encoding="utf-8")
    assert DEMO_SLUG not in cj


def test_step_copy_fixture() -> None:
    """UI with descriptions/dates via temp fixture — does not alter demo CMS data."""
    slug = "ui-fixture-desc-9k2m"
    path = t.TRACK_DIR / f"{slug}.json"
    payload = {
        "projectName": "Fixture Tabela",
        "clientName": "Fixture Client",
        "slug": slug,
        "description": "UI test only",
        "steps": [
            {
                "title": "Tasarım",
                "description": "İlk tasarım çalışması hazırlanarak proje için görsel yön belirlendi.",
                "status": "completed",
                "completedDate": "2026-08-11",
            },
            {
                "title": "Tasarım Onayı",
                "description": "Onaylanan tasarım üretim aşamasına aktarıldı.",
                "status": "completed",
                "completedDate": "2026-08-12",
            },
            {
                "title": "Üretim",
                "description": (
                    "Tabelanın üretimi devam ediyor. "
                    "Üretim tamamlandığında montaj aşamasına geçilecek."
                ),
                "status": "current",
                "completedDate": "2099-01-01",  # must NOT render on current
            },
            {
                "title": "Montaj",
                "description": "Üretim tamamlandıktan sonra montaj gerçekleştirilecek.",
                "status": "pending",
                "completedDate": "",
            },
            {
                "title": "Teslim",
                "description": "",
                "status": "pending",
                "completedDate": "",
            },
        ],
        "currentStep": 3,
        "lastUpdated": "2026-08-13",
        "public": True,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        t.main()
        html = Path(t.OUT_DIR / slug / "index.html").read_text(encoding="utf-8")
        assert "track-now-desc" in html
        assert "Tabelanın üretimi devam ediyor" in html
        assert "İlk tasarım çalışması" in html
        assert "Onaylanan tasarım" in html
        assert "montaj gerçekleştirilecek" in html
        assert "Açıklama yok" not in html
        assert "11 Ağustos 2026" in html
        assert "12 Ağustos 2026" in html
        assert "2099" not in html
        assert "Tamamlandı ·" in html
        assert "track-step-desc" in html
        assert "overflow-wrap" in Path(t.ROOT / "assets" / "site.css").read_text(encoding="utf-8")
        assert html.find("track-now-desc") < html.find("track-timeline")
        assert slug not in Path(t.ROOT / "content.json").read_text(encoding="utf-8")
        assert slug not in Path(t.ROOT / "sitemap.xml").read_text(encoding="utf-8")
    finally:
        path.unlink(missing_ok=True)
        t.main()
        assert not (t.OUT_DIR / slug).exists()
        demo = json.loads((t.TRACK_DIR / f"{DEMO_SLUG}.json").read_text(encoding="utf-8"))
        assert demo.get("slug") == DEMO_SLUG
        assert demo.get("public") is True


def test_public_false_and_slug_orphan() -> None:
    """public:false skips write; orphan slug dirs are removed."""
    demo = t.TRACK_DIR / f"{DEMO_SLUG}.json"
    raw = json.loads(demo.read_text(encoding="utf-8"))
    t.main()
    assert (t.OUT_DIR / DEMO_SLUG / "index.html").exists()

    orphan = t.OUT_DIR / "old-slug-orphan"
    orphan.mkdir(parents=True, exist_ok=True)
    (orphan / "index.html").write_text("x", encoding="utf-8")

    tmp = dict(raw)
    tmp["public"] = False
    demo.write_text(json.dumps(tmp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        t.main()
        assert not (t.OUT_DIR / DEMO_SLUG / "index.html").exists()
        assert not orphan.exists()
    finally:
        demo.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        t.main()
        assert (t.OUT_DIR / DEMO_SLUG / "index.html").exists()


def test_date_format() -> None:
    assert t._format_tr_date("2026-08-13") == "13 Ağustos 2026"
    assert t._format_tr_date("2026-08-13T12:00:00.000Z") == "13 Ağustos 2026"


def main() -> None:
    test_validation()
    test_date_format()
    test_demo_page()
    test_step_copy_fixture()
    test_public_false_and_slug_orphan()
    print("test_project_tracking: PASS (5 suites)")


if __name__ == "__main__":
    main()
