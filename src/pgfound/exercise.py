"""Exercise lookup and runner support."""

from __future__ import annotations

import difflib
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psycopg

from pgfound import paths
from pgfound.content import seed as content_seed
from pgfound.lab.psql import build_argv


@dataclass(frozen=True)
class ExerciseRecord:
    """Resolved exercise files and metadata."""

    data: dict[str, Any]
    path: Path

    @property
    def id(self) -> str:
        return str(self.data["id"])

    @property
    def directory(self) -> Path:
        return self.path.parent

    @property
    def prompt_path(self) -> Path:
        return self.directory / "prompt.md"

    @property
    def solution_path(self) -> Path:
        return self.directory / str(self.data["solution_path"])

    @property
    def answer_path(self) -> Path:
        return paths.REPO_ROOT / "tmp" / "answers" / f"{self.id}.sql"

    @property
    def progress_path(self) -> Path:
        return paths.REPO_ROOT / "tmp" / "progress" / f"{self.id}.json"

    @property
    def seed_domain(self) -> str:
        dataset = self.data.get("dataset", {})
        return str(dataset["seed_pack_id"])


def find_exercise(identifier: str) -> ExerciseRecord:
    """Find an exercise by ID or by a path ending at an exercise directory."""
    candidates: list[ExerciseRecord] = []
    possible_path = paths.EXERCISES_DIR / identifier / "exercise.json"
    if possible_path.is_file():
        return _load_exercise(possible_path)

    for exercise_path in sorted(paths.EXERCISES_DIR.rglob("exercise.json")):
        record = _load_exercise(exercise_path)
        if record.id == identifier or str(
            record.directory.relative_to(paths.EXERCISES_DIR)
        ).endswith(identifier):
            candidates.append(record)

    if not candidates:
        msg = f"exercise {identifier!r} not found"
        raise ValueError(msg)
    if len(candidates) > 1:
        choices = ", ".join(
            str(item.directory.relative_to(paths.EXERCISES_DIR)) for item in candidates
        )
        msg = f"exercise {identifier!r} is ambiguous; use one of: {choices}"
        raise ValueError(msg)
    return candidates[0]


def seed_plan_lines(record: ExerciseRecord) -> list[str]:
    """Return printable seed plan lines for an exercise."""
    plan = content_seed.plan_seed(domain=record.seed_domain, phase="1")
    return [str(path.relative_to(paths.REPO_ROOT)) for path in plan.sql_files]


def auto_seed(record: ExerciseRecord) -> None:
    """Load the phase-1 seed pack for an exercise."""
    plan = content_seed.plan_seed(domain=record.seed_domain, phase="1")
    content_seed.execute_seed(plan, reset=True, generate=False)


def run_psql() -> None:
    """Open interactive psql and return after the learner exits."""
    subprocess.run(build_argv(), cwd=paths.DOCKER_DIR, check=True)


def save_self_assessment(record: ExerciseRecord, assessment: str) -> Path:
    """Persist a lightweight progress record."""
    record.progress_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "exercise_id": record.id,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "self_assessment": assessment,
    }
    record.progress_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return record.progress_path


def check_answer(record: ExerciseRecord) -> tuple[bool, str]:
    """Compare a saved learner answer to the reference solution row set."""
    if not record.answer_path.is_file():
        msg = f"answer file not found: {record.answer_path.relative_to(paths.REPO_ROOT)}"
        raise FileNotFoundError(msg)

    expected = _run_sql(record.solution_path.read_text(encoding="utf-8"))
    actual = _run_sql(record.answer_path.read_text(encoding="utf-8"))
    if expected == actual:
        return True, ""

    diff = difflib.unified_diff(
        expected,
        actual,
        fromfile="solution",
        tofile=str(record.answer_path.relative_to(paths.REPO_ROOT)),
        lineterm="",
    )
    return False, "\n".join(diff)


def _load_exercise(path: Path) -> ExerciseRecord:
    return ExerciseRecord(data=json.loads(path.read_text(encoding="utf-8")), path=path)


def _run_sql(sql: str) -> list[str]:
    rows: list[str] = []
    with psycopg.connect(content_seed.database_url(), autocommit=False) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            if cursor.description is None:
                connection.rollback()
                return []
            for row in cursor.fetchall():
                rows.append(json.dumps([_stringify(value) for value in row], sort_keys=True))
        connection.rollback()
    return sorted(rows)


def _stringify(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
