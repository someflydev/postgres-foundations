from __future__ import annotations

import json

from pgfound import paths
from pgfound.lab import harness


def test_concurrency_scenario_files_parse_and_reference_declared_sessions() -> None:
    scenario_paths = harness.scenario_paths()
    assert {path.name for path in scenario_paths} >= {
        "inventory-lost-update.yaml",
        "inventory-lost-update-fixed-for-update.yaml",
        "appointment-double-booking.yaml",
        "appointment-double-booking-fixed-exclusion.yaml",
        "two-doctors-write-skew.yaml",
        "two-doctors-write-skew-fixed-serializable.yaml",
        "bank-transfer-deadlock.yaml",
        "bank-transfer-ordered-fix.yaml",
        "funds-retry-on-serialization-failure.yaml",
        "check-inventory-for-update.yaml",
        "check-appointment-absence-race.yaml",
        "check-appointment-exclusion-fix.yaml",
        "check-write-skew-serializable.yaml",
        "check-bank-deadlock-opposite-order.yaml",
        "check-bank-ordered-locking.yaml",
        "check-funds-idempotent-retry.yaml",
    }
    for scenario_path in scenario_paths:
        scenario = harness.load_scenario(scenario_path)
        declared_sessions = set(scenario["sessions"])
        for step in scenario["steps"]:
            assert step["session"] in declared_sessions, scenario_path


def test_multi_session_exercise_profiles_use_placeholder_backed_scenarios() -> None:
    for exercise_path in paths.EXERCISES_DIR.glob(
        "phase-06-transactions-concurrency-and-correctness/**/exercise.json"
    ):
        exercise = json.loads(exercise_path.read_text(encoding="utf-8"))
        if exercise.get("expected_output_shape") != "multi_session_trace":
            continue
        scenario_path = harness.find_scenario(exercise["lab_harness_profile"])
        scenario_text = scenario_path.read_text(encoding="utf-8")
        assert harness.LEARNER_SQL_PLACEHOLDER in scenario_text, exercise_path
