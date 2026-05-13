from scenario_industry_helpers import (
    assert_industry_scenarios_valid,
    load_report,
    slugs_by_class_and_kind,
)


def test_fintech_industry_scenarios_validate_and_match_goldens() -> None:
    assert_industry_scenarios_valid("fintech-payments")


def test_fintech_high_volume_flags_missing_restore_drills() -> None:
    report = load_report("fintech-payments", "03-high-volume-trading-adjacent")
    warnings = {warning["anti_pattern_slug"] for warning in report["warnings"]}
    assert "no_restore_drills" in warnings


def test_fintech_high_volume_has_mature_extension_posture() -> None:
    report = load_report("fintech-payments", "03-high-volume-trading-adjacent")
    mature_extensions = slugs_by_class_and_kind(report, "recommend_now", "extension")
    assert {"pg_stat_statements", "pgbouncer"} <= mature_extensions
