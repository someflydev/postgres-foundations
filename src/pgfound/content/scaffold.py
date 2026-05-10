"""Content scaffolding helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pgfound import paths


def phase_directory_name(phase_number: int, *, curriculum_map_path: Path | None = None) -> str:
    map_path = curriculum_map_path or paths.CURRICULUM_DIR / "map.json"
    curriculum = json.loads(map_path.read_text(encoding="utf-8"))
    for phase in curriculum.get("phases", []):
        if phase.get("number") == phase_number:
            return f"phase-{phase_number:02d}-{phase['slug']}"
    msg = f"phase {phase_number} is not present in {map_path}"
    raise ValueError(msg)


def scaffold_lesson(
    *,
    phase: int,
    cluster: str,
    slug: str,
    title: str,
    capability_layer: str,
    curriculum_map_path: Path | None = None,
    lessons_root: Path | None = None,
) -> Path:
    """Create a draft lesson directory from templates and return it."""
    phase_dir = phase_directory_name(phase, curriculum_map_path=curriculum_map_path)
    root = lessons_root or paths.LESSONS_DIR
    lesson_dir = root / phase_dir / cluster / slug
    lesson_dir.mkdir(parents=True, exist_ok=True)

    existing_files = [
        path for path in (lesson_dir / "lesson.json", lesson_dir / "body.md") if path.exists()
    ]
    if existing_files:
        existing = ", ".join(str(path) for path in existing_files)
        msg = f"lesson scaffold target already contains authored files: {existing}"
        raise ValueError(msg)

    template_dir = paths.REPO_ROOT / "content-schemas" / "templates"
    lesson_template = (template_dir / "lesson.json.template").read_text(encoding="utf-8")
    body_template = (template_dir / "lesson-body.md.template").read_text(encoding="utf-8")

    lesson_json = (
        lesson_template.replace("__LESSON_ID__", slug)
        .replace("__TITLE__", title)
        .replace("__PHASE__", str(phase))
        .replace("__CAPABILITY_LAYER__", capability_layer)
    )
    (lesson_dir / "lesson.json").write_text(lesson_json, encoding="utf-8")
    (lesson_dir / "body.md").write_text(body_template, encoding="utf-8")
    return lesson_dir


def scaffold_exercise(
    *,
    lesson: str,
    level: str,
    slug: str,
    kind: str,
    title: str,
    sessions: int = 1,
    lessons_root: Path | None = None,
    exercises_root: Path | None = None,
    curriculum_map_path: Path | None = None,
) -> Path:
    """Create a draft exercise directory and return it."""
    normalized_level = level.upper()
    if normalized_level not in {"A", "B", "C", "D"}:
        msg = "exercise level must be one of: a, b, c, d"
        raise ValueError(msg)
    if sessions < 1:
        msg = "exercise sessions must be at least 1"
        raise ValueError(msg)

    lesson_root = lessons_root or paths.LESSONS_DIR
    lesson_dir = lesson_root / lesson
    lesson_json_path = lesson_dir / "lesson.json"
    if not lesson_json_path.is_file():
        msg = f"lesson {lesson!r} does not resolve to an authored lesson.json"
        raise ValueError(msg)

    lesson_data = json.loads(lesson_json_path.read_text(encoding="utf-8"))
    phase_dir = lesson_dir.relative_to(lesson_root).parts[0]
    exercise_dir = (
        (exercises_root or paths.EXERCISES_DIR)
        / phase_dir
        / lesson_dir.name
        / f"level-{normalized_level.lower()}"
        / slug
    )
    exercise_dir.mkdir(parents=True, exist_ok=True)

    authored_files = [
        exercise_dir / "exercise.json",
        exercise_dir / "prompt.md",
        exercise_dir / "starter.sql",
        exercise_dir / "solution.md",
        exercise_dir / "solution.sql",
    ]
    existing_files = [path for path in authored_files if path.exists()]
    if existing_files:
        existing = ", ".join(str(path) for path in existing_files)
        msg = f"exercise scaffold target already contains authored files: {existing}"
        raise ValueError(msg)

    allowed_concepts = _exercise_allowed_concepts(
        lesson_data=lesson_data,
        lessons_root=lesson_root,
    )
    not_yet_allowed = _exercise_not_yet_allowed_concepts(
        lesson_data=lesson_data,
        lessons_root=lesson_root,
        curriculum_map_path=curriculum_map_path,
    )
    exercise = _exercise_json(
        slug=slug,
        title=title,
        lesson_id=str(lesson_data["id"]),
        level=normalized_level,
        kind=kind,
        sessions=sessions,
        allowed_concepts=allowed_concepts,
        not_yet_allowed_concepts=not_yet_allowed,
    )
    (exercise_dir / "exercise.json").write_text(
        json.dumps(exercise, indent=2) + "\n",
        encoding="utf-8",
    )
    (exercise_dir / "prompt.md").write_text(_prompt_md(exercise), encoding="utf-8")
    if kind != "modeling":
        (exercise_dir / "starter.sql").write_text("-- Optional starter SQL.\n", encoding="utf-8")
    if sessions > 1:
        for index in range(1, sessions + 1):
            (exercise_dir / f"session-script-{index}.sql").write_text(
                f"-- Session {index} script for the multi-session trace.\n",
                encoding="utf-8",
            )
        solution_text = _multi_session_solution_md(sessions)
    else:
        solution_text = "# Reference Solution\n\n__REPLACE_ME__\n"
    (exercise_dir / "solution.md").write_text(solution_text, encoding="utf-8")
    return exercise_dir


def _exercise_json(
    *,
    slug: str,
    title: str,
    lesson_id: str,
    level: str,
    kind: str,
    sessions: int,
    allowed_concepts: list[str],
    not_yet_allowed_concepts: list[str],
) -> dict[str, Any]:
    expected_shape = {
        "A": "prose_explanation",
        "B": "rowset",
        "C": "rowset",
        "D": "prose_explanation",
    }[level]
    time_target = {
        "A": 10,
        "B": 20,
        "C": 30,
        "D": 45,
    }[level]
    exercise: dict[str, Any] = {
        "id": slug,
        "title": title,
        "lesson_id": lesson_id,
        "scaffolding_level": level,
        "kind": kind,
        "allowed_concepts": allowed_concepts,
        "not_yet_allowed_concepts": not_yet_allowed_concepts,
        "schema_scope": {"schemas": ["public"]},
        "dataset": {"seed_pack_id": "default_lab", "max_rows_hint": 0},
        "expected_output_shape": expected_shape,
        "sessions": sessions,
        "success_criteria": ["__REPLACE_ME_SUCCESS_CRITERION__"],
        "time_target_minutes": time_target,
        "rubric_id": _default_rubric_id(kind),
        "solution_path": "solution.md",
        "tags": [],
        "status": "draft",
    }
    if kind != "modeling":
        exercise["starter_path"] = "starter.sql"
    if sessions > 1:
        exercise["expected_output_shape"] = "multi_session_trace"
        exercise["lab_harness_profile"] = "two-session" if sessions == 2 else f"{sessions}-session"
    if level in {"A", "B"}:
        exercise["hints"] = ["__REPLACE_ME_HINT__"]
    if level in {"C", "D"}:
        prompt_count = 2 if level == "C" else 3
        exercise["oral_defense_prompts"] = ["__REPLACE_ME__" for _ in range(prompt_count)]
    return exercise


def _default_rubric_id(kind: str) -> str:
    return {
        "query": "query-correctness",
        "schema": "schema-design",
        "modeling": "schema-design",
        "debug": "critique-and-repair",
        "critique": "critique-and-repair",
        "lab": "query-correctness",
    }[kind]


def _prompt_md(exercise: dict[str, Any]) -> str:
    allowed = "\n".join(f"- {concept}" for concept in exercise["allowed_concepts"]) or "- None"
    not_yet = (
        "\n".join(f"- {concept}" for concept in exercise["not_yet_allowed_concepts"]) or "- None"
    )
    success = "\n".join(f"- {item}" for item in exercise["success_criteria"])
    oral = ""
    if exercise["scaffolding_level"] in {"C", "D"}:
        prompts = "\n".join(f"- {item}" for item in exercise["oral_defense_prompts"])
        oral = f"\n## Oral Defense\n\n{prompts}\n"
    return f"""# {exercise["title"]}

## Setup

Use the PostgreSQL Foundations lab and the `{exercise["dataset"]["seed_pack_id"]}` seed pack.
Enter the lab with `make lab-psql`.

## Given

__REPLACE_ME__

## Task

__REPLACE_ME__

## Allowed Concepts

{allowed}

## Not Yet Allowed

{not_yet}

## Success Criteria

{success}
{oral}
## Estimated Time

{exercise["time_target_minutes"]} minutes.
"""


def _multi_session_solution_md(sessions: int) -> str:
    blocks = "\n".join(
        f"```sql\n-- session {index}\n__REPLACE_ME_SESSION_{index}__\n```"
        for index in range(1, sessions + 1)
    )
    return (
        "# Reference Solution\n\n"
        "Runs against the harness introduced in PROMPT_19.\n\n"
        "## Expected Interleaving\n\n"
        f"{blocks}\n\n"
        "## Outcome\n\n"
        "__REPLACE_ME_OUTCOME__\n"
    )


def _exercise_allowed_concepts(*, lesson_data: dict[str, Any], lessons_root: Path) -> list[str]:
    phase = lesson_data.get("phase")
    concepts: set[str] = set(lesson_data.get("concepts_introduced", []))
    if isinstance(phase, int):
        for other in _lesson_json_files(lessons_root):
            other_data = json.loads(other.read_text(encoding="utf-8"))
            if other_data.get("phase", phase + 1) < phase:
                concepts.update(other_data.get("concepts_introduced", []))
    return sorted(concepts)


def _exercise_not_yet_allowed_concepts(
    *,
    lesson_data: dict[str, Any],
    lessons_root: Path,
    curriculum_map_path: Path | None,
) -> list[str]:
    phase = lesson_data.get("phase")
    concepts: set[str] = set(lesson_data.get("concepts_not_yet_allowed", []))
    if isinstance(phase, int):
        curriculum = json.loads(
            (curriculum_map_path or paths.CURRICULUM_DIR / "map.json").read_text(encoding="utf-8")
        )
        for map_phase in curriculum.get("phases", []):
            if map_phase.get("number", phase) > phase:
                concepts.update(map_phase.get("concepts_introduced", []))
        for other in _lesson_json_files(lessons_root):
            other_data = json.loads(other.read_text(encoding="utf-8"))
            if other_data.get("phase", phase) > phase:
                concepts.update(other_data.get("concepts_introduced", []))
    return sorted(concepts - set(lesson_data.get("concepts_introduced", [])))


def _lesson_json_files(lessons_root: Path) -> list[Path]:
    if not lessons_root.exists():
        return []
    return sorted(path for path in lessons_root.rglob("lesson.json") if path.is_file())
