"""Seed pack sufficiency checks for authored exercises."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pgfound import paths
from pgfound.content import seed

TABLE_REF_RE = re.compile(
    r"\b(?:FROM|JOIN)\s+(?!\()(?:(?P<schema>[a-zA-Z_][a-zA-Z0-9_]*)\.)?"
    r"(?P<table>[a-zA-Z_][a-zA-Z0-9_]*)",
    re.IGNORECASE,
)
CREATE_TABLE_RE = re.compile(
    r"\bCREATE\s+(?:TEMP(?:ORARY)?\s+)?TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+"
    r"(?:(?P<schema>[a-zA-Z_][a-zA-Z0-9_]*)\.)?(?P<table>[a-zA-Z_][a-zA-Z0-9_]*)",
    re.IGNORECASE,
)
CREATE_VIEW_RE = re.compile(
    r"\bCREATE\s+(?:OR\s+REPLACE\s+)?(?:MATERIALIZED\s+)?VIEW\s+"
    r"(?:IF\s+NOT\s+EXISTS\s+)?(?:(?P<schema>[a-zA-Z_][a-zA-Z0-9_]*)\.)?"
    r"(?P<table>[a-zA-Z_][a-zA-Z0-9_]*)",
    re.IGNORECASE,
)
CTE_RE = re.compile(
    r"(?:\bWITH\s+(?:RECURSIVE\s+)?|,\s*)"
    r"(?P<table>[a-zA-Z_][a-zA-Z0-9_]*)\s+AS\s+(?:MATERIALIZED\s+|NOT\s+MATERIALIZED\s+)?\(",
    re.IGNORECASE,
)
SEED_TABLE_RE = re.compile(
    r"\b(?:CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?|INSERT\s+INTO|ALTER\s+TABLE|UPDATE)\s+"
    r"(?:(?P<schema>[a-zA-Z_][a-zA-Z0-9_]*)\.)?(?P<table>[a-zA-Z_][a-zA-Z0-9_]*)",
    re.IGNORECASE,
)
SYSTEM_SCHEMAS = {"information_schema", "pg_catalog", "pgfound"}
NON_TABLE_REFS = {"lateral", "unnest"}


@dataclass(frozen=True)
class SeedDoctorIssue:
    """One seed-data drift issue."""

    exercise_id: str
    path: Path
    seed_pack_id: str
    phase: str
    message: str


@dataclass(frozen=True)
class SeedDoctorReport:
    """Seed doctor result."""

    exercises_checked: int
    issues: tuple[SeedDoctorIssue, ...]

    @property
    def ok(self) -> bool:
        return not self.issues


def run_seed_doctor(
    *,
    exercises_dir: Path | None = None,
    seed_packs_dir: Path | None = None,
) -> SeedDoctorReport:
    """Scan exercises and confirm referenced seed phases/tables exist."""
    exercise_root = exercises_dir or paths.EXERCISES_DIR
    packs_root = seed_packs_dir or paths.SEED_DATA_DIR / "packs"
    issues: list[SeedDoctorIssue] = []
    checked = 0

    for exercise_path in sorted(exercise_root.rglob("exercise.json")):
        checked += 1
        try:
            data = json.loads(exercise_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            issues.append(_issue("<unknown>", exercise_path, "<unknown>", "<unknown>", str(exc)))
            continue

        exercise_id = str(data.get("id", exercise_path.parent.name))
        dataset = data.get("dataset", {})
        seed_pack_id = str(dataset.get("seed_pack_id", ""))
        phase = _exercise_phase(data)
        if not seed_pack_id:
            issues.append(
                _issue(exercise_id, exercise_path, "", phase, "dataset.seed_pack_id missing")
            )
            continue

        pack_phase_dir = packs_root / seed_pack_id / "phases"
        try:
            phase_path = pack_phase_dir / _phase_file_name(phase)
        except ValueError:
            issues.append(
                _issue(
                    exercise_id,
                    exercise_path,
                    seed_pack_id,
                    phase,
                    f"invalid phase: {phase}",
                )
            )
            continue
        if not phase_path.is_file():
            issues.append(
                _issue(
                    exercise_id,
                    exercise_path,
                    seed_pack_id,
                    phase,
                    f"missing referenced phase SQL: phases/{phase_path.name}",
                )
            )
            continue

        seed_tables = _seed_tables(pack_phase_dir, phase)
        solution_path = exercise_path.parent / str(data.get("solution_path", ""))
        if solution_path.name != "solution.sql" or not solution_path.is_file():
            continue
        for table_ref in sorted(_solution_table_refs(solution_path)):
            if _is_external_schema_ref(table_ref, seed_pack_id):
                continue
            if table_ref not in seed_tables:
                issues.append(
                    _issue(
                        exercise_id,
                        exercise_path,
                        seed_pack_id,
                        phase,
                        f"solution references table not found in seed SQL: {table_ref}",
                    )
                )

    return SeedDoctorReport(exercises_checked=checked, issues=tuple(issues))


def _is_external_schema_ref(table_ref: str, seed_pack_id: str) -> bool:
    if "." not in table_ref:
        return False
    schema_name, _ = table_ref.split(".", 1)
    return schema_name != seed.SCHEMA_BY_DOMAIN.get(seed_pack_id)


def _issue(
    exercise_id: str,
    path: Path,
    seed_pack_id: str,
    phase: str,
    message: str,
) -> SeedDoctorIssue:
    return SeedDoctorIssue(
        exercise_id=exercise_id,
        path=path,
        seed_pack_id=seed_pack_id,
        phase=phase,
        message=message,
    )


def _exercise_phase(data: dict[str, Any]) -> str:
    schema_scope = data.get("schema_scope", {})
    if isinstance(schema_scope, dict) and schema_scope.get("phase") is not None:
        return str(schema_scope["phase"])
    return "1"


def _phase_files(pack_phase_dir: Path, phase: str) -> tuple[Path, ...]:
    requested_key = seed.phase_sort_key(phase)
    files = []
    for path in pack_phase_dir.glob("phase-*.sql"):
        match = seed.PHASE_FILE_RE.match(path.name)
        if match and seed.phase_sort_key(match.group("phase")) <= requested_key:
            files.append(path)
    return tuple(sorted(files, key=lambda path: seed.phase_sort_key(seed._phase_from_path(path))))


def _phase_file_name(phase: str) -> str:
    match = re.fullmatch(r"(?P<number>\d+)(?P<suffix>[a-z]?)", phase)
    if match is None:
        msg = f"invalid phase id: {phase}"
        raise ValueError(msg)
    return f"phase-{int(match.group('number')):02d}{match.group('suffix')}.sql"


def _seed_tables(pack_phase_dir: Path, phase: str) -> set[str]:
    tables: set[str] = set()
    for sql_file in _phase_files(pack_phase_dir, phase):
        sql = sql_file.read_text(encoding="utf-8")
        for match in SEED_TABLE_RE.finditer(sql):
            schema = match.group("schema")
            table = match.group("table")
            tables.add(f"{schema}.{table}" if schema else table)
            tables.add(table)
    return tables


def _solution_table_refs(solution_path: Path) -> set[str]:
    sql = solution_path.read_text(encoding="utf-8")
    created = {
        _format_table_ref(match.group("schema"), match.group("table"))
        for match in CREATE_TABLE_RE.finditer(sql)
    }
    created.update(
        _format_table_ref(match.group("schema"), match.group("table"))
        for match in CREATE_VIEW_RE.finditer(sql)
    )
    created.update(match.group("table") for match in CTE_RE.finditer(sql))
    refs: set[str] = set()
    for match in TABLE_REF_RE.finditer(sql):
        schema = match.group("schema")
        table = match.group("table")
        if schema in SYSTEM_SCHEMAS or table.lower() in NON_TABLE_REFS:
            continue
        table_ref = _format_table_ref(schema, table)
        if table_ref in created or table in created:
            continue
        refs.add(table_ref)
    return refs


def _format_table_ref(schema: str | None, table: str) -> str:
    return f"{schema}.{table}" if schema else table
