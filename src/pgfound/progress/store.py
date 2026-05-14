"""Atomic progress storage under tmp/progress."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pgfound import paths
from pgfound.progress.models import (
    CapstoneAttempt,
    ExerciseAttempt,
    InterviewAttempt,
    LearnerProfile,
)


@dataclass(frozen=True)
class ProgressSnapshot:
    profile: LearnerProfile | None
    exercise_attempts: tuple[ExerciseAttempt, ...]
    capstone_attempts: tuple[CapstoneAttempt, ...]
    interview_attempts: tuple[InterviewAttempt, ...]


def progress_root() -> Path:
    return paths.REPO_ROOT / "tmp" / "progress"


def profile_path() -> Path:
    return progress_root() / "profile.json"


def exercise_progress_path(exercise_id: str) -> Path:
    return progress_root() / "exercises" / f"{exercise_id}.json"


def capstone_progress_path(capstone_id: str) -> Path:
    return progress_root() / "capstones" / f"{capstone_id}.json"


def interview_progress_path() -> Path:
    return progress_root() / "interviews.json"


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.name}.tmp")
    tmp_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp_path, path)


def read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.is_file():
        return default
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"progress record must be an object: {path}")
    return data


def write_profile(profile: LearnerProfile) -> Path:
    path = profile_path()
    atomic_write_json(path, profile.to_dict())
    return path


def read_profile(path: Path | None = None) -> LearnerProfile | None:
    resolved = path or profile_path()
    if not resolved.is_file():
        return None
    return LearnerProfile.from_dict(read_json(resolved, {}))


def read_exercise_progress(path: Path) -> dict[str, Any]:
    data = read_json(path, {"exercise_id": path.stem, "attempts": []})
    if not isinstance(data.get("exercise_id"), str):
        raise ValueError(f"invalid progress record, exercise_id must be a string: {path}")
    if not isinstance(data.get("attempts"), list):
        raise ValueError(f"invalid progress record, attempts must be a list: {path}")
    for attempt in data["attempts"]:
        if not isinstance(attempt, dict):
            raise ValueError(f"invalid progress record, attempt must be an object: {path}")
        ExerciseAttempt.from_dict(data["exercise_id"], attempt)
    return data


def write_exercise_progress(exercise_id: str, attempts: list[dict[str, Any]]) -> Path:
    path = exercise_progress_path(exercise_id)
    payload = {"exercise_id": exercise_id, "attempts": attempts}
    read_exercise_progress_payload(path, payload)
    atomic_write_json(path, payload)
    return path


def read_exercise_progress_payload(path: Path, payload: dict[str, Any]) -> None:
    if not isinstance(payload.get("attempts"), list):
        raise ValueError(f"invalid progress record, attempts must be a list: {path}")
    for attempt in payload["attempts"]:
        if not isinstance(attempt, dict):
            raise ValueError(f"invalid progress record, attempt must be an object: {path}")
        ExerciseAttempt.from_dict(str(payload.get("exercise_id", path.stem)), attempt)


def read_capstone_progress(path: Path) -> dict[str, Any]:
    data = read_json(path, {"capstone_id": path.stem, "attempts": []})
    if not isinstance(data.get("capstone_id"), str):
        raise ValueError(f"invalid capstone progress record, capstone_id must be a string: {path}")
    if not isinstance(data.get("attempts"), list):
        raise ValueError(f"invalid capstone progress record, attempts must be a list: {path}")
    for attempt in data["attempts"]:
        if not isinstance(attempt, dict):
            raise ValueError(f"invalid capstone progress record, attempt must be an object: {path}")
        CapstoneAttempt.from_dict(data["capstone_id"], attempt)
    return data


def write_capstone_progress(capstone_id: str, attempts: list[dict[str, Any]]) -> Path:
    path = capstone_progress_path(capstone_id)
    payload = {"capstone_id": capstone_id, "attempts": attempts}
    for attempt in attempts:
        CapstoneAttempt.from_dict(capstone_id, attempt)
    atomic_write_json(path, payload)
    return path


def read_interview_attempts(path: Path | None = None) -> tuple[InterviewAttempt, ...]:
    resolved = path or interview_progress_path()
    data = read_json(resolved, {"attempts": []})
    if not isinstance(data.get("attempts"), list):
        raise ValueError(f"invalid interview progress record, attempts must be a list: {resolved}")
    return tuple(InterviewAttempt.from_dict(item) for item in data["attempts"])


def load_snapshot(root: Path | None = None) -> ProgressSnapshot:
    base = root or progress_root()
    profile = read_profile(base / "profile.json")
    exercise_attempts: list[ExerciseAttempt] = []
    for path in sorted((base / "exercises").glob("*.json")):
        data = read_exercise_progress(path)
        exercise_attempts.extend(
            ExerciseAttempt.from_dict(str(data["exercise_id"]), item) for item in data["attempts"]
        )
    capstone_attempts: list[CapstoneAttempt] = []
    for path in sorted((base / "capstones").glob("*.json")):
        data = read_capstone_progress(path)
        capstone_attempts.extend(
            CapstoneAttempt.from_dict(str(data["capstone_id"]), item) for item in data["attempts"]
        )
    interviews = read_interview_attempts(base / "interviews.json")
    return ProgressSnapshot(
        profile=profile,
        exercise_attempts=tuple(exercise_attempts),
        capstone_attempts=tuple(capstone_attempts),
        interview_attempts=interviews,
    )
