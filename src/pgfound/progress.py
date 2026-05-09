"""Progress record helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pgfound import paths


@dataclass(frozen=True)
class ProgressSummary:
    """Aggregate progress counts."""

    profile_exists: bool
    exercise_files: int
    exercise_attempts: int
    capstone_files: int
    capstone_attempts: int


def progress_root() -> Path:
    return paths.REPO_ROOT / "tmp" / "progress"


def exercise_progress_path(exercise_id: str) -> Path:
    return progress_root() / "exercises" / f"{exercise_id}.json"


def capstone_progress_path(capstone_id: str) -> Path:
    return progress_root() / "capstones" / f"{capstone_id}.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_exercise_attempt(
    exercise_id: str,
    *,
    started_at: str,
    completed_at: str | None = None,
    self_assessment: str = "not_recorded",
    check_result: str = "not_run",
    notes: str = "",
) -> Path:
    """Append one exercise attempt in the canonical tmp/progress format."""
    path = exercise_progress_path(exercise_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = read_exercise_progress(path)
    payload["exercise_id"] = exercise_id
    payload.setdefault("attempts", []).append(
        {
            "started_at": started_at,
            "completed_at": completed_at or utc_now(),
            "self_assessment": self_assessment,
            "check_result": check_result,
            "notes": notes,
        }
    )
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def read_exercise_progress(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exercise_id": path.stem, "attempts": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data.get("attempts"), list):
        msg = f"invalid progress record, attempts must be a list: {path}"
        raise ValueError(msg)
    return data


def summarize(root: Path | None = None) -> ProgressSummary:
    """Read tmp/progress and return a minimal summary."""
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
        data = json.loads(path.read_text(encoding="utf-8"))
        attempts = data.get("attempts", [])
        if isinstance(attempts, list):
            capstone_attempts += len(attempts)

    return ProgressSummary(
        profile_exists=(base / "profile.json").is_file(),
        exercise_files=exercise_files,
        exercise_attempts=exercise_attempts,
        capstone_files=capstone_files,
        capstone_attempts=capstone_attempts,
    )
