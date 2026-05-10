from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-06-transactions-concurrency-and-correctness"
PHASE6_LESSONS = {
    "what-a-transaction-is",
    "begin-commit-rollback-and-error-handling",
    "mvcc-in-30-minutes",
    "read-committed-is-the-default",
    "repeatable-read-and-snapshot-isolation",
    "serializable-and-predicate-locking",
    "lost-update",
    "write-skew",
    "phantom-reads-and-range-checks",
    "select-for-update-vs-for-no-key-update",
    "why-deadlocks-happen-and-how-to-avoid-them",
    "making-operations-safe-to-retry",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase6_lessons_and_exercises_validate_and_lint_cleanly() -> None:
    report = validate.validate_content(
        path_globs=(
            f"lessons/{PHASE_DIR}/**/lesson.json",
            f"exercises/{PHASE_DIR}/**/exercise.json",
            "rubrics/default/*.rubric.json",
            "curriculum/map.json",
        )
    )
    assert report.ok, [issue.message for issue in report.errors]

    lint_report = lint.lint_content(
        path_globs=(
            f"lessons/{PHASE_DIR}/**/lesson.json",
            f"exercises/{PHASE_DIR}/**/exercise.json",
        )
    )
    assert lint_report.ok, [issue.message for issue in lint_report.warnings]


def test_phase6_has_required_lessons_and_exercises() -> None:
    lesson_paths = sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"))
    assert {path.parent.name for path in lesson_paths} == PHASE6_LESSONS
    assert len(lesson_paths) == 12

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) == 96
    for lesson_path in lesson_paths:
        lesson = _load_json(lesson_path)
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 700
        assert len(exercises_by_lesson[lesson["id"]]) == 8


def test_phase6_required_drills_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / PHASE_DIR).glob("**/*")
        if path.is_file() and path.suffix in {".md", ".sql", ".json"}
    )
    assert "Reproduce a lost update in two psql sessions; fix it with FOR UPDATE" in exercise_text
    assert (
        "Reproduce write skew in REPEATABLE READ and show that SERIALIZABLE prevents it"
        in exercise_text
    )
    assert (
        "silently allows double-booking because the check-then-insert pattern has no row lock"
        in exercise_text
    )
    assert "update the same two rows in opposite orders" in exercise_text
    assert "Runs against the harness introduced in PROMPT_19" in exercise_text


def test_phase6_multi_session_exercises_have_harness_metadata() -> None:
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("**/exercise.json"):
        exercise = _load_json(exercise_path)
        if exercise.get("expected_output_shape") == "multi_session_trace":
            assert exercise.get("sessions", 1) > 1
            assert isinstance(exercise.get("lab_harness_profile"), str)
            assert exercise["lab_harness_profile"]


def test_phase6_domain_sql_matches_prompt_contracts() -> None:
    ecommerce_sql = (paths.SEED_DATA_DIR / "packs/ecommerce/phases/phase-06.sql").read_text(
        encoding="utf-8"
    )
    scheduling_sql = (paths.SEED_DATA_DIR / "packs/scheduling/phases/phase-06.sql").read_text(
        encoding="utf-8"
    )

    assert "CREATE TABLE IF NOT EXISTS ecommerce.inventory" in ecommerce_sql
    assert "CREATE TABLE IF NOT EXISTS ecommerce.order_reservations" in ecommerce_sql
    assert "CREATE TABLE IF NOT EXISTS bank.funds_transfer" in ecommerce_sql
    assert "CREATE TABLE IF NOT EXISTS scheduling.appointment_holds" in scheduling_sql
