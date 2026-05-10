from __future__ import annotations

import shutil

import psycopg
import pytest

from pgfound.content import seed as content_seed
from pgfound.lab import harness

pytestmark = pytest.mark.docker


def _skip_without_lab() -> None:
    if shutil.which("docker") is None:
        pytest.skip("Docker CLI is not available")
    try:
        with psycopg.connect(content_seed.database_url(), connect_timeout=1) as connection:
            connection.execute("SELECT 1")
    except psycopg.OperationalError as exc:
        pytest.skip(f"PostgreSQL lab is not reachable: {exc}")


def test_tiny_harness_scenario_exercises_rows_rowcount_and_error_code() -> None:
    _skip_without_lab()
    scenario = {
        "name": "tiny-harness-test",
        "sessions": {
            "A": {"role": "pgfound", "database": "pgfound"},
        },
        "setup_sql": """
            CREATE SCHEMA IF NOT EXISTS pgfound_harness;
            DROP TABLE IF EXISTS pgfound_harness.tiny;
            CREATE TABLE pgfound_harness.tiny (
                id integer PRIMARY KEY,
                label text NOT NULL
            );
            INSERT INTO pgfound_harness.tiny VALUES (1, 'one');
        """,
        "steps": [
            {
                "session": "A",
                "sql": "SELECT label FROM pgfound_harness.tiny WHERE id = 1;",
                "expect": {"rows": [{"label": "one"}]},
            },
            {
                "session": "A",
                "sql": "UPDATE pgfound_harness.tiny SET label = 'uno' WHERE id = 1;",
                "expect": {"rowcount": 1},
            },
            {
                "session": "A",
                "sql": "INSERT INTO pgfound_harness.tiny VALUES (1, 'duplicate');",
                "expect": {"error_code": "23505"},
            },
        ],
        "teardown_sql": "DROP TABLE IF EXISTS pgfound_harness.tiny;",
    }

    report = harness.run_scenario(scenario)

    assert report.ok, report.diff
