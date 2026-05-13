from scenario_industry_helpers import (
    assert_industry_scenarios_valid,
    industry_scenario_dirs,
    load_report,
    slugs_by_class,
    slugs_by_class_and_kind,
)


def test_saas_industry_scenarios_validate_and_match_goldens() -> None:
    assert_industry_scenarios_valid("saas-multi-tenant")


def test_saas_progression_covers_tenant_isolation_spectrum() -> None:
    tenancy_models = [
        (scenario_dir / "scenario.json").read_text(encoding="utf-8")
        for scenario_dir in industry_scenario_dirs("saas-multi-tenant")
    ]
    assert "shared schema" in tenancy_models[0]
    assert "schema per tenant" in tenancy_models[1]
    assert "schema per tenant" in tenancy_models[2]


def test_saas_progression_has_required_decision_posture() -> None:
    early = load_report("saas-multi-tenant", "01-early-stage-crm")
    early_now = slugs_by_class(early, "recommend_now")
    assert {"pg_stat_statements", "constraints", "row_level_security"} <= early_now

    mature = load_report("saas-multi-tenant", "03-multi-region-saas-compliance")
    mature_extensions = slugs_by_class_and_kind(mature, "recommend_now", "extension")
    assert {"pg_stat_statements", "pgbouncer"} <= mature_extensions
    warnings = {warning["anti_pattern_slug"] for warning in mature["warnings"]}
    assert "shard_without_distribution_key" in warnings
    assert "citus" in slugs_by_class(mature, "candidate_later")
