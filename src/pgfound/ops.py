"""Operational query helpers for the PostgreSQL lab."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psycopg
from rich.console import Console
from rich.table import Table

from pgfound import paths
from pgfound.content.seed import database_url

MONITORING_DIR = paths.REPO_ROOT / "scripts" / "monitoring"


@dataclass(frozen=True)
class QueryResult:
    name: str
    columns: tuple[str, ...]
    rows: tuple[tuple[Any, ...], ...]


def query_names() -> tuple[str, ...]:
    """Return available monitoring query names without the .sql suffix."""
    return tuple(sorted(path.stem for path in MONITORING_DIR.glob("*.sql")))


def query_path(name: str) -> Path:
    """Resolve a monitoring query by canonical name."""
    safe_name = name.removesuffix(".sql")
    if "/" in safe_name or "\\" in safe_name or safe_name in {"", ".", ".."}:
        msg = f"invalid monitoring query name: {name}"
        raise ValueError(msg)
    path = MONITORING_DIR / f"{safe_name}.sql"
    if not path.is_file():
        available = ", ".join(query_names()) or "none"
        msg = f"unknown monitoring query {name!r}; available: {available}"
        raise FileNotFoundError(msg)
    return path


def run_query(name: str) -> QueryResult:
    """Run a canonical monitoring SQL script against the configured lab."""
    path = query_path(name)
    sql = path.read_text(encoding="utf-8")
    with psycopg.connect(database_url()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = tuple(column.name for column in (cursor.description or ()))
            rows = tuple(tuple(row) for row in cursor.fetchall()) if cursor.description else ()
    return QueryResult(name=path.stem, columns=columns, rows=rows)


def render_result(console: Console, result: QueryResult) -> None:
    """Render a monitoring query result as a Rich table."""
    table = Table(title=f"ops query: {result.name}")
    for column in result.columns:
        table.add_column(column)
    for row in result.rows:
        table.add_row(*(str(value) if value is not None else "" for value in row))
    console.print(table)
