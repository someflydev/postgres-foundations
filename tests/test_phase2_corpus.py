from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

PHASE_DIR = "phase-02-relational-joins-and-aggregation"
LEVEL_D_PATTERNS = re.compile(
    r"duplicates|incorrect count|missing rows|wrong aggregation", re.IGNORECASE
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase2_lessons_and_exercises_validate_and_lint_cleanly() -> None:
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


def test_phase2_clusters_have_planned_lesson_count() -> None:
    curriculum = _load_json(paths.CURRICULUM_DIR / "map.json")
    phase2 = next(phase for phase in curriculum["phases"] if phase["number"] == 2)
    lessons_by_cluster: dict[str, list[Path]] = defaultdict(list)

    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lessons_by_cluster[lesson_path.parent.parent.name].append(lesson_path)

    for cluster in phase2["clusters"]:
        assert len(lessons_by_cluster[cluster["slug"]]) == cluster["planned_lessons"]


def test_phase2_exercises_have_required_levels_and_level_d_language() -> None:
    exercises_by_lesson_and_level: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson_and_level[
            (exercise["lesson_id"], exercise["scaffolding_level"])
        ].append(exercise_path)
        solution = exercise_path.parent / "solution.sql"
        assert solution.is_file()
        assert ";" in solution.read_text(encoding="utf-8")
        assert exercise.get("output_comparison") in {"ordered", "unordered", "multiset"}

        if exercise["scaffolding_level"] == "D":
            prompt = (exercise_path.parent / "prompt.md").read_text(encoding="utf-8")
            assert LEVEL_D_PATTERNS.search(prompt), exercise_path

    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lesson = _load_json(lesson_path)
        assert len(exercises_by_lesson_and_level[(lesson["id"], "A")]) == 2
        assert len(exercises_by_lesson_and_level[(lesson["id"], "B")]) == 2
        assert len(exercises_by_lesson_and_level[(lesson["id"], "C")]) == 2
        assert len(exercises_by_lesson_and_level[(lesson["id"], "D")]) == 1


def test_phase2_group_by_lessons_have_non_aggregated_column_drill() -> None:
    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lesson = _load_json(lesson_path)
        if "group_by" not in lesson.get("concepts_introduced", []):
            continue

        prompts = [
            (exercise_path.parent / "prompt.md").read_text(encoding="utf-8").lower()
            for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR / lesson["id"] / "level-d").glob(
                "*/exercise.json"
            )
        ]
        assert any("non-aggregated selected columns" in prompt for prompt in prompts)
