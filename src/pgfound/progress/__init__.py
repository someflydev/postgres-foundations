"""Progress record helpers and package API."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pgfound import paths
from pgfound.progress import derive, remediation, reports, store
from pgfound.progress.models import (
    CapstoneAttempt,
    ExerciseAttempt,
    InterviewAttempt,
    LearnerProfile,
    ModuleProgress,
)


@dataclass(frozen=True)
class ProgressSummary:
    profile_exists: bool
    exercise_files: int
    exercise_attempts: int
    capstone_files: int
    capstone_attempts: int


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def progress_root() -> Path:
    return store.progress_root()


def exercise_progress_path(exercise_id: str) -> Path:
    return store.exercise_progress_path(exercise_id)


def capstone_progress_path(capstone_id: str) -> Path:
    return store.capstone_progress_path(capstone_id)


def append_exercise_attempt(
    exercise_id: str,
    *,
    started_at: str,
    completed_at: str | None = None,
    self_assessment: str = "not_recorded",
    check_result: str = "not_run",
    rubric_scores: dict[str, int | float] | None = None,
    notes: str = "",
) -> Path:
    path = exercise_progress_path(exercise_id)
    payload = store.read_exercise_progress(path)
    attempt = ExerciseAttempt(
        exercise_id=exercise_id,
        started_at=started_at,
        completed_at=completed_at or utc_now(),
        self_assessment=self_assessment,
        check_result=check_result,
        rubric_scores=rubric_scores or {},
        notes=notes,
    )
    attempts = list(payload.setdefault("attempts", []))
    attempts.append(attempt.to_attempt_dict())
    return store.write_exercise_progress(exercise_id, attempts)


def read_exercise_progress(path: Path) -> dict[str, Any]:
    return store.read_exercise_progress(path)


def summarize(root: Path | None = None) -> ProgressSummary:
    base = root or progress_root()
    exercise_files = 0
    exercise_attempts = 0
    for path in sorted((base / "exercises").glob("*.json")):
        exercise_files += 1
        exercise_attempts += len(read_exercise_progress(path).get("attempts", []))

    capstone_files = 0
    capstone_attempts = 0
    for path in sorted((base / "capstones").glob("*.json")):
        capstone_files += 1
        capstone_attempts += len(store.read_capstone_progress(path).get("attempts", []))

    return ProgressSummary(
        profile_exists=(base / "profile.json").is_file(),
        exercise_files=exercise_files,
        exercise_attempts=exercise_attempts,
        capstone_files=capstone_files,
        capstone_attempts=capstone_attempts,
    )


__all__ = [
    "CapstoneAttempt",
    "ExerciseAttempt",
    "InterviewAttempt",
    "LearnerProfile",
    "ModuleProgress",
    "ProgressSummary",
    "append_exercise_attempt",
    "capstone_progress_path",
    "derive",
    "exercise_progress_path",
    "paths",
    "progress_root",
    "read_exercise_progress",
    "remediation",
    "reports",
    "store",
    "summarize",
    "utc_now",
]
