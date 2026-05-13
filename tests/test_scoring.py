from pgfound.decision import scoring


def test_score_action_applies_penalties_and_weights() -> None:
    intake = {
        "organization": {
            "team_size_engineers": 4,
            "operational_tolerance": "low",
            "managed_service_requirement": "mandatory",
            "portability_constraints": ["any_managed"],
        },
        "security_constraints": [],
        "scale_signals": {
            "row_counts_largest_tables": {"events": 25_000_000},
            "write_throughput_rows_per_sec": 150,
            "read_throughput_qps": 300,
            "concurrent_connections_peak": 80,
            "growth_rate_month_over_month": 0.1,
        },
    }
    action = {
        "kind": "extension",
        "target_slug": "timescaledb",
        "confidence": 0.8,
        "scoring": {
            "domain_fit": 0.8,
            "data_shape_fit": 0.9,
            "workload_fit": 0.85,
            "operational_feasibility": 0.7,
            "growth_urgency": 0.4,
            "portability_penalty": 0.05,
            "complexity_penalty": 0.2,
        },
    }
    catalog_entry = {
        "operational_cost": "High cost because jobs and compression need ownership.",
        "managed_service_availability": "limited",
    }

    result = scoring.score_action(action, intake, catalog_entry)

    assert 0 <= result["recommendation_score"] <= 1
    assert result["score_breakdown"]["portability_penalty"] >= 0.24
    assert result["score_breakdown"]["complexity_penalty"] >= 0.72
    assert result["score_breakdown"]["operational_feasibility"] < 0.7


def test_score_action_boosts_required_rls_fit() -> None:
    intake = {
        "organization": {
            "team_size_engineers": 12,
            "operational_tolerance": "low",
            "managed_service_requirement": "mandatory",
            "portability_constraints": ["aws_rds"],
        },
        "security_constraints": ["rls_required"],
        "scale_signals": {
            "row_counts_largest_tables": {"audit": 20_000_000},
            "write_throughput_rows_per_sec": 200,
            "read_throughput_qps": 1500,
            "concurrent_connections_peak": 200,
            "growth_rate_month_over_month": 0.12,
        },
    }
    action = {
        "kind": "core_feature",
        "target_slug": "row_level_security",
        "confidence": 0.88,
        "scoring": {
            "domain_fit": 0.86,
            "data_shape_fit": 0.82,
            "workload_fit": 0.84,
            "operational_feasibility": 0.76,
            "growth_urgency": 0.5,
            "portability_penalty": 0.03,
            "complexity_penalty": 0.25,
        },
    }

    result = scoring.score_action(action, intake, {})

    assert result["recommendation_score"] >= 0.7
    assert result["score_breakdown"]["domain_fit"] > 0.86
