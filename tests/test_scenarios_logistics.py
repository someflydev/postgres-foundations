from scenario_industry_helpers import (
    assert_industry_scenarios_valid,
    load_report,
    slugs_by_class,
)


def test_logistics_industry_scenarios_validate_and_match_goldens() -> None:
    assert_industry_scenarios_valid("logistics-geo")


def test_logistics_postgis_and_timescale_posture_progresses_by_scale() -> None:
    small = load_report("logistics-geo", "01-last-mile-delivery-single-city")
    assert {"postgis", "gist_geospatial"} <= slugs_by_class(small, "recommend_now")

    regional = load_report("logistics-geo", "02-multi-region-logistics-with-zones")
    assert {"postgis", "partitioning", "brin_append_only_chronological"} <= slugs_by_class(
        regional, "recommend_now"
    )
    assert "timescaledb" in slugs_by_class(regional, "candidate_later")

    global_fleet = load_report("logistics-geo", "03-global-fleet-analytics")
    assert {"postgis", "timescaledb", "partitioning"} <= slugs_by_class(
        global_fleet, "recommend_now"
    )
