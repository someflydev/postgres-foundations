from scenario_industry_helpers import (
    assert_industry_scenarios_valid,
    load_report,
    slugs_by_class,
)


def test_observability_industry_scenarios_validate_and_match_goldens() -> None:
    assert_industry_scenarios_valid("observability-iot")


def test_observability_timescale_and_vector_posture_is_grounded() -> None:
    internal = load_report("observability-iot", "01-internal-observability-500-services")
    assert {"partitioning", "brin_append_only_chronological"} <= slugs_by_class(
        internal, "recommend_now"
    )
    assert "timescaledb" in slugs_by_class(internal, "candidate_later")

    telemetry = load_report("observability-iot", "02-iot-fleet-telemetry-10k-devices")
    assert "timescaledb" in slugs_by_class(telemetry, "recommend_now")

    incident_ops = load_report("observability-iot", "03-real-time-incident-ops-platform")
    assert "pgvector" in slugs_by_class(incident_ops, "not_enough_evidence")
