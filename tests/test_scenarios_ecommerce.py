from scenario_industry_helpers import (
    assert_industry_scenarios_valid,
    load_report,
    slugs_by_class,
    slugs_by_class_and_kind,
)


def test_ecommerce_industry_scenarios_validate_and_match_goldens() -> None:
    assert_industry_scenarios_valid("ecommerce-marketplace")


def test_marketplace_sellers_scenario_recommends_partitioning_consideration() -> None:
    report = load_report("ecommerce-marketplace", "02-marketplace-with-many-sellers")
    now_or_later = slugs_by_class(report, "recommend_now") | slugs_by_class(
        report, "candidate_later"
    )
    assert {"partitioning", "brin_append_only_chronological"} <= now_or_later


def test_ecommerce_cross_border_has_mature_extension_posture() -> None:
    report = load_report("ecommerce-marketplace", "03-cross-border-ecommerce-compliance")
    mature_extensions = slugs_by_class_and_kind(report, "recommend_now", "extension")
    assert {"pg_stat_statements", "pgbouncer"} <= mature_extensions
