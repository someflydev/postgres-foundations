from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-01-sql-literacy-basics"
FORBIDDEN_SQL_PATTERNS = {
    "join": re.compile(r"\bjoin\b", re.IGNORECASE),
    "group_by": re.compile(r"\bgroup\s+by\b", re.IGNORECASE),
    "aggregate": re.compile(r"\b(count|sum|avg|min|max)\s*\(", re.IGNORECASE),
    "cte": re.compile(r"\bwith\b", re.IGNORECASE),
    "window_function": re.compile(r"\bover\s*\(", re.IGNORECASE),
    "transaction": re.compile(r"\b(begin|commit|rollback)\b", re.IGNORECASE),
    "index": re.compile(r"\bindex\b", re.IGNORECASE),
    "foreign_key": re.compile(r"\bforeign\s+key\b", re.IGNORECASE),
    "primary_key": re.compile(r"\bprimary\s+key\b", re.IGNORECASE),
    "function_definitions": re.compile(r"\bcreate\s+function\b", re.IGNORECASE),
    "jsonb": re.compile(r"\bjsonb\b", re.IGNORECASE),
    "array": re.compile(r"\barray\b|\[\]", re.IGNORECASE),
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase1_lessons_validate_and_lint_cleanly() -> None:
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


def test_phase1_clusters_have_exact_lesson_count() -> None:
    curriculum = _load_json(paths.CURRICULUM_DIR / "map.json")
    phase1 = next(phase for phase in curriculum["phases"] if phase["number"] == 1)
    lessons_by_cluster: dict[str, list[Path]] = defaultdict(list)

    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lessons_by_cluster[lesson_path.parent.parent.name].append(lesson_path)

    for cluster in phase1["clusters"]:
        assert len(lessons_by_cluster[cluster["slug"]]) == cluster["planned_lessons"]


def test_phase1_exercises_have_required_levels_and_solution_sql() -> None:
    exercises_by_lesson_and_level: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson_and_level[
            (exercise["lesson_id"], exercise["scaffolding_level"])
        ].append(exercise_path)
        solution = exercise_path.parent / "solution.sql"
        assert solution.is_file()
        sql = solution.read_text(encoding="utf-8")
        assert ";" in sql
        for concept in exercise["not_yet_allowed_concepts"]:
            pattern = FORBIDDEN_SQL_PATTERNS.get(concept)
            if pattern is not None:
                assert pattern.search(sql) is None, (exercise_path, concept)

    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lesson = _load_json(lesson_path)
        assert len(exercises_by_lesson_and_level[(lesson["id"], "A")]) == 2
        assert len(exercises_by_lesson_and_level[(lesson["id"], "B")]) == 2
        assert len(exercises_by_lesson_and_level[(lesson["id"], "C")]) == 2
        assert len(exercises_by_lesson_and_level[(lesson["id"], "D")]) == 1
