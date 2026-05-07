"""Content scaffolding helpers."""

from __future__ import annotations

import json
from pathlib import Path

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
