"""Database-backed capstone review helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import psycopg

from pgfound.review.models import Finding, Signal
from pgfound.review.normalize import normalize_for_comparison

PSQL_SET_RE = re.compile(r"^\\set\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s+(?P<value>.+)$")
PSQL_VAR_RE = re.compile(r":'(?P<name>[A-Za-z_][A-Za-z0-9_]*)'")


def run_full_capstone_checks(
    *,
    learner_dir: Path,
    reference_dir: Path,
    critical_queries_path: str,
    db_url: str | None,
) -> tuple[list[Signal], list[Finding], list[dict[str, Any]]]:
    """Apply learner artifacts and compare critical-query outputs in a rollback."""
    if not db_url:
        return (
            [Signal("capstone_database_checks", "skipped", "No database URL was provided.")],
            [
                Finding(
                    "warning",
                    "Capstone database checks skipped",
                    "No database URL was provided for full capstone evaluation.",
                    str(learner_dir),
                )
            ],
            [],
        )

    reference_queries = reference_dir / "critical-queries.sql"
    learner_queries = learner_dir / critical_queries_path
    findings: list[Finding] = []
    signals: list[Signal] = []
    comparisons: list[dict[str, Any]] = []

    try:
        with psycopg.connect(db_url, autocommit=False) as connection:
            with connection.cursor() as cursor:
                _apply_artifacts(cursor, learner_dir)
                reference_outputs = _run_query_file(cursor, reference_queries)
                learner_outputs = _run_query_file(cursor, learner_queries)
                comparisons = _compare_outputs(reference_outputs, learner_outputs)
            connection.rollback()
    except psycopg.OperationalError as exc:
        return (
            [
                Signal(
                    "capstone_database_checks",
                    "skipped",
                    str(exc),
                    str(learner_dir),
                )
            ],
            [
                Finding(
                    "warning",
                    "Capstone database checks skipped",
                    str(exc),
                    str(learner_dir),
                    "Lab hygiene",
                )
            ],
            comparisons,
        )
    except Exception as exc:
        return (
            [
                Signal(
                    "capstone_database_checks",
                    "failed",
                    str(exc),
                    str(learner_dir),
                )
            ],
            [
                Finding(
                    "error",
                    "Capstone database checks failed",
                    str(exc),
                    str(learner_dir),
                    "Lab hygiene",
                )
            ],
            comparisons,
        )

    mismatches = [item for item in comparisons if not item["matches"]]
    signals.append(
        Signal(
            "capstone_database_checks",
            "present",
            "Schema, indexes, RLS, and critical queries executed in a rollback.",
            str(learner_dir),
        )
    )
    signals.append(
        Signal(
            "critical_query_outputs_match",
            "present" if not mismatches else "missing",
            f"{len(mismatches)} critical-query output mismatch(es).",
            str(learner_queries),
        )
    )
    if mismatches:
        findings.append(
            Finding(
                "error",
                "Critical-query outputs differ from reference",
                f"{len(mismatches)} statement(s) returned different normalized output.",
                str(learner_queries),
                "Query Correctness: Result semantics",
            )
        )
    else:
        findings.append(
            Finding(
                "info",
                "Critical-query outputs match reference",
                "Reference and learner critical-query files returned the same normalized outputs.",
                str(learner_queries),
                "Query Correctness: Result semantics",
            )
        )
    return signals, findings, comparisons


def _apply_artifacts(cursor: psycopg.Cursor[Any], learner_dir: Path) -> None:
    for filename in ("schema.sql", "indexes.sql", "rls-policies.sql"):
        path = learner_dir / filename
        if path.is_file():
            _execute_all(cursor, path.read_text(encoding="utf-8"))


def _run_query_file(cursor: psycopg.Cursor[Any], path: Path) -> list[list[str]]:
    if not path.is_file():
        msg = f"critical query file not found: {path}"
        raise FileNotFoundError(msg)
    sql = _preprocess_psql_vars(path.read_text(encoding="utf-8"))
    outputs: list[list[str]] = []
    for statement in _split_statements(sql):
        if not statement.strip():
            continue
        cursor.execute(statement)
        outputs.append(_fetch_all_result_sets(cursor))
    return outputs


def _execute_all(cursor: psycopg.Cursor[Any], sql: str) -> None:
    for statement in _split_statements(_preprocess_psql_vars(sql)):
        if not statement.strip():
            continue
        cursor.execute(statement)
        while cursor.nextset():
            pass


def _fetch_all_result_sets(cursor: psycopg.Cursor[Any]) -> list[str]:
    rows: list[str] = []
    while True:
        if cursor.description is not None:
            rows.extend(
                json.dumps([normalize_for_comparison(value) for value in row], sort_keys=True)
                for row in cursor.fetchall()
            )
        if not cursor.nextset():
            break
    return sorted(rows)


def _compare_outputs(left: list[list[str]], right: list[list[str]]) -> list[dict[str, Any]]:
    count = max(len(left), len(right))
    comparisons: list[dict[str, Any]] = []
    for index in range(count):
        reference = left[index] if index < len(left) else []
        learner = right[index] if index < len(right) else []
        comparisons.append(
            {
                "statement_index": index + 1,
                "matches": reference == learner,
                "reference_rows": len(reference),
                "learner_rows": len(learner),
            }
        )
    return comparisons


def _preprocess_psql_vars(sql: str) -> str:
    variables: dict[str, str] = {}
    kept_lines: list[str] = []
    for line in sql.splitlines():
        match = PSQL_SET_RE.match(line.strip())
        if match:
            variables[match.group("name")] = _sql_literal(match.group("value"))
            continue
        kept_lines.append(line)

    processed = "\n".join(kept_lines)

    def replace(match: re.Match[str]) -> str:
        name = match.group("name")
        if name not in variables:
            msg = f"psql variable {name!r} was referenced but not set"
            raise ValueError(msg)
        return variables[name]

    return PSQL_VAR_RE.sub(replace, processed)


def _sql_literal(raw: str) -> str:
    stripped = raw.strip()
    if stripped.startswith("'") and stripped.endswith("'"):
        return stripped
    return "'" + stripped.replace("'", "''") + "'"


def _split_statements(sql: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    in_single_quote = False
    dollar_tag: str | None = None
    index = 0
    while index < len(sql):
        char = sql[index]
        if dollar_tag:
            if sql.startswith(dollar_tag, index):
                current.append(dollar_tag)
                index += len(dollar_tag)
                dollar_tag = None
                continue
            current.append(char)
            index += 1
            continue

        if not in_single_quote and char == "$":
            tag_match = re.match(r"\$[A-Za-z_][A-Za-z0-9_]*\$|\$\$", sql[index:])
            if tag_match:
                dollar_tag = tag_match.group(0)
                current.append(dollar_tag)
                index += len(dollar_tag)
                continue

        if char == "'" and not dollar_tag:
            current.append(char)
            if in_single_quote and index + 1 < len(sql) and sql[index + 1] == "'":
                current.append("'")
                index += 2
                continue
            in_single_quote = not in_single_quote
            index += 1
            continue

        if char == ";" and not in_single_quote and not dollar_tag:
            statements.append("".join(current).strip())
            current = []
            index += 1
            continue

        current.append(char)
        index += 1

    tail = "".join(current).strip()
    if tail:
        statements.append(tail)
    return statements
