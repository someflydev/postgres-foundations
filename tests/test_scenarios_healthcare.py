import json

from scenario_industry_helpers import (
    assert_industry_scenarios_valid,
    load_report,
    slugs_by_class,
    slugs_by_class_and_kind,
)

from pgfound import paths


def test_healthcare_industry_scenarios_validate_and_match_goldens() -> None:
    assert_industry_scenarios_valid("healthcare-ops")


def test_healthcare_scenarios_include_hipaa_and_audit_posture() -> None:
    scenario_root = paths.SCENARIOS_DIR / "industries" / "healthcare-ops"
    intakes = [
        json.loads(path.read_text(encoding="utf-8")) for path in scenario_root.glob("*/intake.json")
    ]
    assert any("hipaa" in intake["security_constraints"] for intake in intakes)
    assert all("audit_required" in intake["security_constraints"] for intake in intakes)
    hospital = load_report("healthcare-ops", "02-hospital-system-audit-heavy")
    why_now = " ".join(
        " ".join(recommendation["why_now"]) for recommendation in hospital["recommendations"]
    )
    assert "audit_required posture" in why_now


def test_healthcare_mature_scenario_has_core_and_extension_now() -> None:
    report = load_report("healthcare-ops", "03-telehealth-appointment-platform")
    assert {"constraints", "row_level_security", "partitioning"} <= slugs_by_class(
        report, "recommend_now"
    )
    mature_extensions = slugs_by_class_and_kind(report, "recommend_now", "extension")
    assert {"pg_stat_statements", "pgbouncer"} <= mature_extensions
