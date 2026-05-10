from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-05-expressive-querying"
PHASE5_LESSONS = {
    "what-a-cte-is",
    "chained-ctes-for-staged-logic",
    "recursive-ctes",
    "what-window-functions-are",
    "running-totals-and-rank",
    "lead-lag-and-time-series-feel",
    "what-lateral-unlocks",
    "insert-on-conflict",
    "exists-and-not-exists",
    "what-a-view-is-for",
    "when-a-materialized-view-helps",
    "synthesis-choosing-the-right-shape",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase5_lessons_and_exercises_validate_and_lint_cleanly() -> None:
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


def test_phase5_has_required_lessons_and_minimum_exercises() -> None:
    lesson_paths = sorted((paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"))
    assert {path.parent.name for path in lesson_paths} == PHASE5_LESSONS
    assert len(lesson_paths) == 12

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    assert sum(len(items) for items in exercises_by_lesson.values()) >= 80
    assert sum(len(items) for items in exercises_by_lesson.values()) == 96
    for lesson_path in lesson_paths:
        lesson = _load_json(lesson_path)
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 600
        assert len(exercises_by_lesson[lesson["id"]]) == 8


def test_phase5_required_drills_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / PHASE_DIR).glob("**/*")
        if path.is_file() and path.suffix in {".md", ".sql", ".json"}
    )
    assert "NULL values" in exercise_text
    assert "wrong frame clause" in exercise_text
    assert "ON CONFLICT DO NOTHING" in exercise_text
    assert "stale materialized view" in exercise_text
    assert "per-customer top 3 orders by revenue" in exercise_text
    assert "ROW_NUMBER() approach" in exercise_text


def test_phase5_domain_sql_matches_prompt_contracts() -> None:
    ecommerce_sql = (paths.SEED_DATA_DIR / "packs/ecommerce/phases/phase-05.sql").read_text(
        encoding="utf-8"
    )
    scheduling_sql = (paths.SEED_DATA_DIR / "packs/scheduling/phases/phase-05.sql").read_text(
        encoding="utf-8"
    )
    saas_sql = (paths.SEED_DATA_DIR / "packs/saas_multi_tenant/phases/phase-05.sql").read_text(
        encoding="utf-8"
    )
    events_sql = (paths.SEED_DATA_DIR / "packs/event_heavy_ops/phases/phase-05.sql").read_text(
        encoding="utf-8"
    )

    assert "generate_series(1, 2400)" in ecommerce_sql
    assert "generate_series(1, 501)" in scheduling_sql
    assert "generate_series(1, 50)" in saas_sql
    assert "CREATE TABLE IF NOT EXISTS saas.usage_events" in saas_sql
    assert "generate_series(1, 50000)" in events_sql
