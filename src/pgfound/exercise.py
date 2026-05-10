"""Exercise lookup and runner support."""

from __future__ import annotations

import difflib
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psycopg

from pgfound import paths, progress
from pgfound.content import seed as content_seed
from pgfound.lab.psql import build_argv
from pgfound.review.normalize import normalize_for_comparison


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
        return progress.exercise_progress_path(self.id)

    @property
    def seed_domain(self) -> str:
        dataset = self.data.get("dataset", {})
        return str(dataset["seed_pack_id"])

    @property
    def seed_phase(self) -> str:
        schema_scope = self.data.get("schema_scope", {})
        return str(schema_scope.get("phase", "1"))

    @property
    def output_comparison(self) -> str:
        return str(self.data.get("output_comparison", "unordered"))

    @property
    def expected_output_shape(self) -> str:
        return str(self.data.get("expected_output_shape", "rowset"))

    @property
    def search_path(self) -> str:
        return str(self.data.get("search_path", "pgfound, public"))


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
    plan = content_seed.plan_seed(domain=record.seed_domain, phase=record.seed_phase)
    return [str(path.relative_to(paths.REPO_ROOT)) for path in plan.sql_files]


def auto_seed(record: ExerciseRecord) -> None:
    """Load the requested seed pack phase for an exercise."""
    plan = content_seed.plan_seed(domain=record.seed_domain, phase=record.seed_phase)
    content_seed.execute_seed(plan, reset=True, generate=False)


def run_psql(search_path: str | None = None) -> None:
    """Open interactive psql and return after the learner exits."""
    subprocess.run(build_argv(search_path=search_path), cwd=paths.DOCKER_DIR, check=True)


def save_attempt(
    record: ExerciseRecord,
    *,
    started_at: str,
    self_assessment: str = "not_recorded",
    check_result: str = "not_run",
    notes: str = "",
) -> Path:
    """Persist a canonical exercise progress attempt."""
    return progress.append_exercise_attempt(
        record.id,
        started_at=started_at,
        self_assessment=self_assessment,
        check_result=check_result,
        notes=notes,
    )


def check_answer(
    record: ExerciseRecord, answer_path: Path | None = None, *, timing: bool = False
) -> tuple[bool, str]:
    """Compare a saved learner answer to the reference solution row set."""
    correct, diff, _ = check_answer_with_timing(record, answer_path=answer_path, timing=timing)
    return correct, diff


def check_answer_with_timing(
    record: ExerciseRecord, answer_path: Path | None = None, *, timing: bool = False
) -> tuple[bool, str, dict[str, float]]:
    """Compare a saved learner answer and optionally report execution timings."""
    if record.expected_output_shape == "multi_session_trace":
        return True, "multi_session_trace comparison is reserved for the concurrency phase.", {}

    resolved_answer_path = answer_path or record.answer_path
    if not resolved_answer_path.is_file():
        msg = f"answer file not found: {_relative_path(resolved_answer_path)}"
        raise FileNotFoundError(msg)

    if record.expected_output_shape == "schema_object":
        expected_sql = record.solution_path.read_text(encoding="utf-8")
        actual_sql = resolved_answer_path.read_text(encoding="utf-8")
        expected, expected_seconds = _time_call(
            lambda: _schema_object_shape(record, expected_sql), enabled=timing
        )
        actual, actual_seconds = _time_call(
            lambda: _schema_object_shape(record, actual_sql), enabled=timing
        )
        timings = _timing_payload(expected_seconds, actual_seconds)
        if expected == actual:
            return True, "", timings
        diff = difflib.unified_diff(
            expected,
            actual,
            fromfile="solution schema",
            tofile=_relative_path(resolved_answer_path),
            lineterm="",
        )
        return False, "\n".join(diff), timings

    expected_rows, expected_seconds = _time_call(
        lambda: _run_sql(
            record.solution_path.read_text(encoding="utf-8"), search_path=record.search_path
        ),
        enabled=timing,
    )
    actual_rows, actual_seconds = _time_call(
        lambda: _run_sql(
            resolved_answer_path.read_text(encoding="utf-8"), search_path=record.search_path
        ),
        enabled=timing,
    )
    expected = _normalize_rows(expected_rows, comparison=record.output_comparison)
    actual = _normalize_rows(actual_rows, comparison=record.output_comparison)
    timings = _timing_payload(expected_seconds, actual_seconds)
    if expected == actual:
        return True, "", timings

    diff = difflib.unified_diff(
        expected,
        actual,
        fromfile="solution",
        tofile=_relative_path(resolved_answer_path),
        lineterm="",
    )
    return False, "\n".join(diff), timings


def _time_call[T](callback: Any, *, enabled: bool) -> tuple[T, float]:
    started = time.perf_counter()
    result = callback()
    if not enabled:
        return result, 0.0
    return result, time.perf_counter() - started


def _timing_payload(expected_seconds: float, actual_seconds: float) -> dict[str, float]:
    if expected_seconds == 0.0 and actual_seconds == 0.0:
        return {}
    return {"solution_seconds": expected_seconds, "answer_seconds": actual_seconds}


def save_answer_from_history(record: ExerciseRecord) -> Path:
    """Best-effort copy of the last SQL statement from ~/.psql_history."""
    history_path = Path.home() / ".psql_history"
    if not history_path.is_file():
        msg = f"psql history not found: {history_path}"
        raise FileNotFoundError(msg)
    statement = _last_history_statement(history_path.read_text(encoding="utf-8"))
    if not statement:
        msg = f"no SQL statement found in {history_path}"
        raise ValueError(msg)
    record.answer_path.parent.mkdir(parents=True, exist_ok=True)
    record.answer_path.write_text(statement.rstrip() + "\n", encoding="utf-8")
    return record.answer_path


def _load_exercise(path: Path) -> ExerciseRecord:
    return ExerciseRecord(data=json.loads(path.read_text(encoding="utf-8")), path=path)


def _run_sql(sql: str, *, search_path: str | None = None) -> list[str]:
    last_rows: list[str] = []
    with psycopg.connect(content_seed.database_url(), autocommit=False) as connection:
        with connection.cursor() as cursor:
            if search_path:
                cursor.execute(f"SET search_path TO {search_path}")
            cursor.execute(sql)
            while True:
                if cursor.description is not None:
                    last_rows = [
                        json.dumps([_normalize_value(value) for value in row], sort_keys=True)
                        for row in cursor.fetchall()
                    ]
                if not cursor.nextset():
                    break
        connection.rollback()
    return last_rows


def _schema_object_shape(record: ExerciseRecord, sql: str) -> list[str]:
    """Run schema SQL in a rolled-back transaction and capture catalog shape."""
    tables = _schema_scope_tables(record)
    with psycopg.connect(content_seed.database_url(), autocommit=False) as connection:
        with connection.cursor() as cursor:
            if record.search_path:
                cursor.execute(f"SET search_path TO {record.search_path}")
            cursor.execute(sql)
            while cursor.nextset():
                pass
            rows = _catalog_rows(cursor, tables)
        connection.rollback()
    return rows


def _schema_scope_tables(record: ExerciseRecord) -> list[tuple[str, str]]:
    """Return fully qualified tables from an exercise schema_scope."""
    schema_scope = record.data.get("schema_scope", {})
    raw_tables = schema_scope.get("tables", []) if isinstance(schema_scope, dict) else []
    tables: list[tuple[str, str]] = []
    for raw_table in raw_tables:
        if not isinstance(raw_table, str) or "." not in raw_table:
            continue
        schema_name, table_name = raw_table.split(".", 1)
        tables.append((schema_name, table_name))
    if not tables:
        msg = "schema_object checks require schema_scope.tables with schema-qualified names"
        raise ValueError(msg)
    return tables


def _catalog_rows(cursor: psycopg.Cursor[Any], tables: list[tuple[str, str]]) -> list[str]:
    rows: list[str] = []
    for schema_name, table_name in tables:
        cursor.execute(
            """
            SELECT
                'column' AS object_kind,
                table_schema,
                table_name,
                column_name,
                ordinal_position::text,
                is_nullable,
                data_type,
                COALESCE(column_default, '')
            FROM information_schema.columns
            WHERE table_schema = %s
              AND table_name = %s
            ORDER BY ordinal_position
            """,
            (schema_name, table_name),
        )
        rows.extend(
            json.dumps([_normalize_value(value) for value in row], sort_keys=True)
            for row in cursor.fetchall()
        )

        cursor.execute(
            """
            SELECT
                'constraint' AS object_kind,
                tc.table_schema,
                tc.table_name,
                tc.constraint_name,
                tc.constraint_type,
                COALESCE(kcu.column_name, ''),
                COALESCE(kcu.ordinal_position::text, '')
            FROM information_schema.table_constraints AS tc
            LEFT JOIN information_schema.key_column_usage AS kcu
              ON kcu.constraint_schema = tc.constraint_schema
             AND kcu.constraint_name = tc.constraint_name
             AND kcu.table_schema = tc.table_schema
             AND kcu.table_name = tc.table_name
            WHERE tc.table_schema = %s
              AND tc.table_name = %s
              AND tc.constraint_name !~ '_not_null$'
            ORDER BY
                tc.constraint_type,
                tc.constraint_name,
                kcu.ordinal_position NULLS LAST,
                kcu.column_name
            """,
            (schema_name, table_name),
        )
        rows.extend(
            json.dumps([_normalize_value(value) for value in row], sort_keys=True)
            for row in cursor.fetchall()
        )
    return sorted(rows)


def _normalize_rows(rows: list[str], *, comparison: str) -> list[str]:
    if comparison == "ordered":
        return rows
    if comparison == "multiset":
        return sorted(rows)
    return sorted(set(rows))


def _normalize_value(value: object) -> object:
    return normalize_for_comparison(value)


def _last_history_statement(history: str) -> str:
    lines = [line for line in history.splitlines() if line.strip() and not line.startswith("\\")]
    collected: list[str] = []
    for line in reversed(lines):
        collected.insert(0, line)
        if line.rstrip().endswith(";"):
            break
    return "\n".join(collected).strip()


def _relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(paths.REPO_ROOT))
    except ValueError:
        return str(path)
