"""Derive module progress from local attempts and authored content."""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pgfound import paths
from pgfound.progress.models import ExerciseAttempt, ModuleProgress

PASSING_CHECK_RESULTS = {"correct", "passed", "pass", "ok"}


@dataclass(frozen=True)
class ExerciseMeta:
    id: str
    lesson_id: str
    level: str
    module_id: str
    path: Path


@dataclass(frozen=True)
class LessonMeta:
    id: str
    module_id: str
    cluster_id: str
    title: str
    exercise_ids: tuple[str, ...]
    path: Path


def load_exercise_meta() -> dict[str, ExerciseMeta]:
    records: dict[str, ExerciseMeta] = {}
    for path in sorted(paths.EXERCISES_DIR.rglob("exercise.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        exercise_id = str(data["id"])
        tags = {str(tag) for tag in data.get("tags", [])}
        schema_scope = data.get("schema_scope", {})
        module_id = _module_id_from_path_or_data(path, data, tags, schema_scope)
        records[exercise_id] = ExerciseMeta(
            id=exercise_id,
            lesson_id=str(data.get("lesson_id", "")),
            level=str(data.get("scaffolding_level", "")).upper(),
            module_id=module_id,
            path=path,
        )
    return records


def load_lesson_meta() -> dict[str, LessonMeta]:
    exercises_by_lesson: dict[str, list[str]] = defaultdict(list)
    for exercise in load_exercise_meta().values():
        if exercise.lesson_id:
            exercises_by_lesson[exercise.lesson_id].append(exercise.id)

    lessons: dict[str, LessonMeta] = {}
    for path in sorted(paths.LESSONS_DIR.rglob("lesson.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        lesson_id = str(data["id"])
        tags = {str(tag) for tag in data.get("tags", [])}
        module_id = _module_id_from_path_or_data(path, data, tags, data)
        configured = []
        for key in ("guided_exercise_ids", "independent_exercise_ids", "critique_exercise_ids"):
            configured.extend(str(item) for item in data.get(key, []))
        lessons[lesson_id] = LessonMeta(
            id=lesson_id,
            module_id=module_id,
            cluster_id=_cluster_id_from_path(path),
            title=str(data.get("title", lesson_id)),
            exercise_ids=tuple(configured or sorted(exercises_by_lesson.get(lesson_id, []))),
            path=path,
        )
    return lessons


def all_module_ids() -> list[str]:
    ids = {lesson.module_id for lesson in load_lesson_meta().values()}
    ids.update(_map_module_ids(paths.CURRICULUM_DIR / "admin" / "map.json"))
    ids.update(_map_module_ids(paths.CURRICULUM_DIR / "extensions" / "map.json"))
    return sorted(ids, key=_module_sort_key)


def compute_module_progress(
    attempts: tuple[ExerciseAttempt, ...] | list[ExerciseAttempt],
) -> dict[str, ModuleProgress]:
    """Mark a module met when every lesson cluster has a passing Level D attempt."""
    exercises = load_exercise_meta()
    lessons = load_lesson_meta()
    passing_exercise_ids = {
        attempt.exercise_id
        for attempt in attempts
        if _attempt_passed(attempt) and exercises.get(attempt.exercise_id, None)
    }
    touched: dict[str, list[ExerciseAttempt]] = defaultdict(list)
    for attempt in attempts:
        meta = exercises.get(attempt.exercise_id)
        if meta:
            touched[meta.module_id].append(attempt)

    module_clusters: dict[str, dict[str, list[LessonMeta]]] = defaultdict(lambda: defaultdict(list))
    for lesson in lessons.values():
        module_clusters[lesson.module_id][lesson.cluster_id].append(lesson)

    progress: dict[str, ModuleProgress] = {}
    for module_id in all_module_ids():
        module_attempts = sorted(
            touched.get(module_id, []), key=lambda item: item.completed_at or item.started_at
        )
        evidence: list[str] = []
        required_clusters = module_clusters.get(module_id, {})
        met_clusters = 0
        for cluster_id, cluster_lessons in required_clusters.items():
            level_d_ids = []
            for lesson in cluster_lessons:
                level_d_ids.extend(
                    exercise_id
                    for exercise_id in lesson.exercise_ids
                    if exercises.get(exercise_id) and exercises[exercise_id].level == "D"
                )
            passed = sorted(set(level_d_ids) & passing_exercise_ids)
            if passed:
                met_clusters += 1
                evidence.append(f"{cluster_id}: {passed[0]}")
        status = "not-started"
        exit_met_at = None
        if module_attempts:
            status = "in-progress"
        if required_clusters and met_clusters == len(required_clusters):
            status = "met"
            exit_met_at = module_attempts[-1].completed_at or module_attempts[-1].started_at
        progress[module_id] = ModuleProgress(
            module_id=module_id,
            status=status,
            first_touched_at=module_attempts[0].started_at if module_attempts else None,
            exit_met_at=exit_met_at,
            evidence=tuple(evidence),
        )
    return progress


def _attempt_passed(attempt: ExerciseAttempt) -> bool:
    if attempt.check_result.lower() in PASSING_CHECK_RESULTS:
        return True
    if not attempt.rubric_scores:
        return False
    valid_scores = [score for score in attempt.rubric_scores.values() if score >= 0]
    return bool(valid_scores) and sum(valid_scores) / len(valid_scores) >= 3


def _module_id_from_path_or_data(
    path: Path, data: dict[str, Any], tags: set[str], schema_scope: dict[str, Any]
) -> str:
    parts = path.relative_to(paths.REPO_ROOT).parts
    for part in parts:
        if part.startswith("phase-"):
            return "-".join(part.split("-")[:2])
    if len(parts) > 2 and parts[1] == "admin":
        return parts[2]
    if len(parts) > 2 and parts[1] == "extensions":
        return parts[2]
    if "phase" in data:
        return _phase_module_id(data["phase"])
    if "phase" in schema_scope:
        return _phase_module_id(schema_scope["phase"])
    for tag in tags:
        if tag.startswith("phase-"):
            return _phase_module_id(tag.removeprefix("phase-"))
    return "unmapped"


def _cluster_id_from_path(path: Path) -> str:
    parts = path.relative_to(paths.LESSONS_DIR).parts
    if not parts:
        return path.parent.name
    if parts[0].startswith("phase-") and len(parts) >= 2:
        return parts[1]
    return path.parent.name


def _map_module_ids(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(module["id"]) for module in data.get("modules", [])}


def _module_sort_key(module_id: str) -> tuple[int, str]:
    if module_id.startswith("phase-"):
        return (0, module_id)
    if module_id.startswith("a"):
        return (1, module_id)
    if module_id.startswith("e"):
        return (2, module_id)
    return (3, module_id)


def _phase_module_id(value: object) -> str:
    phase = str(value)
    if phase.isdigit():
        return f"phase-{int(phase):02d}"
    if len(phase) > 1 and phase[:-1].isdigit():
        return f"phase-{int(phase[:-1]):02d}{phase[-1]}"
    return f"phase-{phase}"
