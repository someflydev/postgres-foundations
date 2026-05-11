from __future__ import annotations

import psycopg
import pytest
from click.testing import CliRunner

from pgfound import ops, paths
from pgfound.cli import main
from pgfound.content.seed import database_url

EXPECTED_COLUMNS = {
    "top-by-total-time": {"queryid", "calls", "total_exec_time_ms", "mean_exec_time_ms"},
    "blocking-chain": {"waiting_pid", "blocking_pid", "waiting_query", "blocking_query"},
    "unused-indexes": {"schemaname", "table_name", "index_name", "idx_scan"},
    "replica-lag": {"replication_kind", "name", "byte_lag", "apply_time_lag"},
    "table-sizes": {"schema_name", "table_name", "total_size", "total_bytes"},
}


def _lab_connection() -> psycopg.Connection:
    try:
        return psycopg.connect(database_url(), connect_timeout=1)
    except psycopg.OperationalError as exc:
        pytest.skip(f"PostgreSQL lab is not running: {exc}")


def test_monitoring_query_registry_lists_scripts() -> None:
    assert set(ops.query_names()) == set(EXPECTED_COLUMNS)
    for name in EXPECTED_COLUMNS:
        path = ops.query_path(name)
        assert path == paths.REPO_ROOT / "scripts" / "monitoring" / f"{name}.sql"
        assert path.read_text(encoding="utf-8").startswith("-- Purpose:")


@pytest.mark.docker
def test_monitoring_sql_scripts_execute_with_expected_columns() -> None:
    with _lab_connection() as connection:
        for name, expected in EXPECTED_COLUMNS.items():
            sql = ops.query_path(name).read_text(encoding="utf-8")
            with connection.cursor() as cursor:
                cursor.execute(sql)
                columns = {column.name for column in cursor.description or ()}
                assert expected <= columns
                cursor.fetchall()


def test_ops_query_cli_reports_unknown_query_without_database() -> None:
    result = CliRunner().invoke(main, ["ops", "query", "missing-query"])

    assert result.exit_code != 0
    assert "unknown monitoring query" in result.output
