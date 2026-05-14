import json
from pathlib import Path

import pytest

from pgfound import paths
from pgfound.decision.engine import DecisionValidationError, run_decision


def test_intake_schema_loads_and_examples_validate() -> None:
    schema_path = paths.DECISION_ENGINE_DIR / "schemas" / "intake.schema.json"
    assert json.loads(schema_path.read_text(encoding="utf-8"))["$schema"].endswith("2020-12/schema")

    for intake_path in (paths.DECISION_ENGINE_DIR / "fixtures" / "intakes").glob("*.json"):
        report = run_decision(intake_path)
        assert report["intake_id"] == intake_path.stem


def test_invalid_intake_fails(tmp_path: Path) -> None:
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text(
        json.dumps(
            {
                "intake_id": "invalid",
                "as_of_date": "2026-05-12",
                "organization": {
                    "industry": "saas_multi_tenant",
                    "team_size_engineers": -1,
                    "operational_tolerance": "extreme",
                    "managed_service_requirement": "mandatory",
                    "portability_constraints": ["aws_rds"],
                },
                "data_shapes": [],
                "workload_patterns": ["oltp_heavy"],
                "scale_signals": {
                    "row_counts_largest_tables": {},
                    "write_throughput_rows_per_sec": 1,
                    "read_throughput_qps": 1,
                    "concurrent_connections_peak": 1,
                    "growth_rate_month_over_month": 2,
                },
                "tenancy_model": "single_tenant",
                "security_constraints": [],
                "migration_or_federation_needs": {
                    "has_legacy_postgres_source": False,
                    "has_legacy_non_postgres_source": False,
                    "requires_zero_downtime_migration": False,
                    "requires_federation_via_fdw": False,
                },
                "explicit_bias_against": [],
                "explicit_bias_for": [],
                "existing_postgres_topology": "none",
                "free_form_notes": "",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(DecisionValidationError):
        run_decision(invalid_path)


def test_intake_extension_bias_slugs_must_exist(tmp_path: Path) -> None:
    base_path = (
        paths.DECISION_ENGINE_DIR / "fixtures" / "intakes" / "saas-multi-tenant-minimal.json"
    )
    intake = json.loads(base_path.read_text(encoding="utf-8"))
    intake["explicit_bias_for"] = [
        {"extension_slug": "not_a_real_extension", "reason": "Regression guard."}
    ]
    invalid_path = tmp_path / "invalid-extension-bias.json"
    invalid_path.write_text(json.dumps(intake), encoding="utf-8")

    with pytest.raises(DecisionValidationError, match="explicit_bias_for"):
        run_decision(invalid_path)

    intake["explicit_bias_for"] = []
    intake["explicit_bias_against"] = [
        {"extension_slug": "still_not_real", "reason": "Regression guard."}
    ]
    invalid_path.write_text(json.dumps(intake), encoding="utf-8")

    with pytest.raises(DecisionValidationError, match="explicit_bias_against"):
        run_decision(invalid_path)
