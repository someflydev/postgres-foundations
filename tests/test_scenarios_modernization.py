from scenario_industry_helpers import (
    assert_industry_scenarios_valid,
    load_report,
    slugs_by_class,
)


def test_modernization_industry_scenarios_validate_and_match_goldens() -> None:
    assert_industry_scenarios_valid("modernization-bridge")


def test_modernization_bridge_recommends_migration_tools_without_sharding() -> None:
    carveout = load_report("modernization-bridge", "01-legacy-monolith-carveout")
    assert "postgres_fdw" in slugs_by_class(carveout, "recommend_now")
    assert "citus" in slugs_by_class(carveout, "avoid_for_now")

    consolidation = load_report("modernization-bridge", "02-multi-database-consolidation")
    assert {"logical_replication", "postgres_fdw"} <= slugs_by_class(consolidation, "recommend_now")

    upgrade = load_report("modernization-bridge", "03-near-zero-downtime-major-upgrade")
    assert {
        "logical_replication",
        "logical_replication_pair",
        "blue_green_upgrade_via_logical_replication",
        "pg_stat_statements",
        "pg_partman",
    } <= (slugs_by_class(upgrade, "recommend_now") | slugs_by_class(upgrade, "candidate_later"))
