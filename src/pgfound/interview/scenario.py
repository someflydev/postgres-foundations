"""Interview scenario loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from pgfound import paths


@dataclass(frozen=True)
class InterviewStage:
    """One timed interview stage."""

    kind: str
    budget_minutes: int
    prompt_template: str | None = None
    topic: str | None = None
    exercise_id: str | None = None


@dataclass(frozen=True)
class InterviewScenario:
    """Resolved interview scenario metadata."""

    id: str
    title: str
    duration_minutes: int
    capability_layers_required: tuple[str, ...]
    stages: tuple[InterviewStage, ...]
    rubric_id: str
    path: Path


def scenario_dir() -> Path:
    """Return the interview scenario directory."""

    return paths.SCENARIOS_DIR / "interviews"


def scenario_paths() -> list[Path]:
    """Return authored interview scenario files."""

    directory = scenario_dir()
    if not directory.is_dir():
        return []
    return sorted(path for path in directory.glob("*.yaml") if path.is_file())


def load_scenario(identifier: str) -> InterviewScenario:
    """Load an interview scenario by ID or file stem."""

    candidates = []
    for path in scenario_paths():
        data = _read_yaml(path)
        if data.get("id") == identifier or path.stem == identifier:
            candidates.append((path, data))

    if not candidates:
        msg = f"interview scenario {identifier!r} not found"
        raise ValueError(msg)
    if len(candidates) > 1:
        msg = f"interview scenario {identifier!r} is ambiguous"
        raise ValueError(msg)
    path, data = candidates[0]
    return _from_data(path, data)


def _read_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        msg = f"scenario must be a YAML object: {path}"
        raise ValueError(msg)
    return loaded


def _from_data(path: Path, data: dict[str, Any]) -> InterviewScenario:
    stages = tuple(
        InterviewStage(
            kind=str(stage["kind"]),
            budget_minutes=int(stage["budget_minutes"]),
            prompt_template=stage.get("prompt_template"),
            topic=stage.get("topic"),
            exercise_id=stage.get("exercise_id"),
        )
        for stage in data.get("stages", [])
        if isinstance(stage, dict)
    )
    return InterviewScenario(
        id=str(data["id"]),
        title=str(data["title"]),
        duration_minutes=int(data["duration_minutes"]),
        capability_layers_required=tuple(str(item) for item in data["capability_layers_required"]),
        stages=stages,
        rubric_id=str(data["rubric_id"]),
        path=path,
    )
