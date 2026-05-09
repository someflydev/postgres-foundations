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

    if record.expected_output_shape == "schema_object":
        expected = _schema_object_shape(record, record.solution_path.read_text(encoding="utf-8"))
        actual = _schema_object_shape(record, record.answer_path.read_text(encoding="utf-8"))
        if expected == actual:
            return True, ""
        diff = difflib.unified_diff(
            expected,
            actual,
            fromfile="solution schema",
            tofile=str(record.answer_path.relative_to(paths.REPO_ROOT)),
            lineterm="",
        )
        return False, "\n".join(diff)

    expected = _normalize_rows(
        _run_sql(record.solution_path.read_text(encoding="utf-8")),
        comparison=record.output_comparison,
    )
    actual = _normalize_rows(
        _run_sql(record.answer_path.read_text(encoding="utf-8")),
        comparison=record.output_comparison,
    )
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
    last_rows: list[str] = []
    with psycopg.connect(content_seed.database_url(), autocommit=False) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            while True:
                if cursor.description is not None:
                    last_rows = [
                        json.dumps([_stringify(value) for value in row], sort_keys=True)
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
        rows.extend(json.dumps([_stringify(value) for value in row]) for row in cursor.fetchall())

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
        rows.extend(json.dumps([_stringify(value) for value in row]) for row in cursor.fetchall())
    return sorted(rows)


def _normalize_rows(rows: list[str], *, comparison: str) -> list[str]:
    if comparison == "ordered":
        return rows
    if comparison == "multiset":
        return sorted(rows)
    return sorted(set(rows))


def _stringify(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
