from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from pgfound import paths

PHASE_DIR = "phase-00-reality-before-syntax"
FORBIDDEN_PHASE0_INTRODUCTIONS = {
    "select",
    "insert",
    "foreign_key",
    "primary_key",
    "normalization",
    "join",
    "index",
    "transaction",
    "constraint",
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase0_clusters_have_planned_lesson_count() -> None:
    curriculum = _load_json(paths.CURRICULUM_DIR / "map.json")
    phase0 = next(phase for phase in curriculum["phases"] if phase["number"] == 0)
    lessons_by_cluster: dict[str, list[Path]] = defaultdict(list)

    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        cluster = lesson_path.parent.parent.name
        lessons_by_cluster[cluster].append(lesson_path)

    for cluster in phase0["clusters"]:
        assert len(lessons_by_cluster[cluster["slug"]]) >= 2


def test_phase0_lessons_have_each_exercise_level() -> None:
    exercises_by_lesson_and_level: dict[tuple[str, str], list[Path]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        exercises_by_lesson_and_level[
            (exercise["lesson_id"], exercise["scaffolding_level"])
        ].append(exercise_path)

    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lesson = _load_json(lesson_path)
        for level in ("A", "B", "C", "D"):
            assert exercises_by_lesson_and_level[(lesson["id"], level)]


def test_phase0_lessons_do_not_introduce_not_yet_allowed_concepts() -> None:
    for lesson_path in (paths.LESSONS_DIR / PHASE_DIR).glob("*/*/lesson.json"):
        lesson = _load_json(lesson_path)
        introduced = set(lesson.get("concepts_introduced", []))
        assert introduced.isdisjoint(FORBIDDEN_PHASE0_INTRODUCTIONS)
        assert introduced.isdisjoint(set(lesson.get("concepts_not_yet_allowed", [])))


def test_phase0_exercises_reference_valid_rubrics() -> None:
    rubric_ids = {
        _load_json(path)["id"] for path in paths.RUBRICS_DIR.rglob("*.json") if path.is_file()
    }
    for exercise_path in (paths.EXERCISES_DIR / PHASE_DIR).glob("*/*/*/exercise.json"):
        exercise = _load_json(exercise_path)
        assert exercise["rubric_id"] in rubric_ids
