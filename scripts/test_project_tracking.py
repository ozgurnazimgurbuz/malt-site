#!/usr/bin/env python3
"""Self-check for project tracking builder. Exit 1 on failure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_project_tracking as t  # noqa: E402


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
    html = Path(t.OUT_DIR / "mantar-garage-7f3k9x" / "index.html").read_text(encoding="utf-8")
    assert "Mantar Garage" in html
    assert "Mantar Garage Tabela" in html
    assert "noindex, nofollow" in html
    assert "Üretim" in html
    assert "Şu anda bu aşamadayız." in html
    assert "13 Ağustos 2026" in html
    assert "Son güncelleme" in html
    assert "wa.me" in html
    assert "tel:+905525826959" in html
    assert "Teklif Al" not in html
    assert html.count('data-status="completed"') == 2
    assert html.count('data-status="current"') == 1
    assert html.count('data-status="pending"') == 2
    assert not (t.OUT_DIR / "index.html").exists()
    assert "/proje/" not in Path(t.ROOT / "sitemap.xml").read_text(encoding="utf-8")
    assert "Disallow: /proje/" in Path(t.ROOT / "robots.txt").read_text(encoding="utf-8")
    cj = Path(t.ROOT / "content.json").read_text(encoding="utf-8")
    assert "mantar-garage" not in cj


def test_public_false_and_slug_orphan() -> None:
    """public:false skips write; orphan slug dirs are removed."""
    demo = t.TRACK_DIR / "mantar-garage-7f3k9x.json"
    raw = json.loads(demo.read_text(encoding="utf-8"))
    # Ensure page exists first
    t.main()
    assert (t.OUT_DIR / "mantar-garage-7f3k9x" / "index.html").exists()

    # Simulate old slug left behind
    orphan = t.OUT_DIR / "old-slug-orphan"
    orphan.mkdir(parents=True, exist_ok=True)
    (orphan / "index.html").write_text("x", encoding="utf-8")

    # public false → not in keep → demo HTML removed; orphan removed
    tmp = dict(raw)
    tmp["public"] = False
    demo.write_text(json.dumps(tmp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        t.main()
        assert not (t.OUT_DIR / "mantar-garage-7f3k9x" / "index.html").exists()
        assert not orphan.exists()
    finally:
        demo.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        t.main()
        assert (t.OUT_DIR / "mantar-garage-7f3k9x" / "index.html").exists()


def test_date_format() -> None:
    assert t._format_tr_date("2026-08-13") == "13 Ağustos 2026"
    assert t._format_tr_date("2026-08-13T12:00:00.000Z") == "13 Ağustos 2026"


def main() -> None:
    test_validation()
    test_date_format()
    test_demo_page()
    test_public_false_and_slug_orphan()
    print("test_project_tracking: PASS (4 suites)")


if __name__ == "__main__":
    main()
