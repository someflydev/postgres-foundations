from __future__ import annotations

import importlib.util

import psycopg
import pytest

from pgfound import paths
from pgfound.content import seed as content_seed


def _load_generator():
    generator_path = paths.SEED_DATA_DIR / "packs/document_search/generators/documents_csv.py"
    spec = importlib.util.spec_from_file_location("documents_csv", generator_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_document_generator_yields_expected_row_count() -> None:
    module = _load_generator()
    rows = list(module.iter_rows())
    assert len(rows) == 5000
    assert rows[0]["id"] == "00000000-0000-0000-0000-000000000001"
    assert rows[-1]["id"] == "00000000-0000-0000-0000-000000005000"


def test_document_generator_has_hits_for_postgres_indexing_query() -> None:
    module = _load_generator()
    rows = list(module.iter_rows())
    hits = [
        row
        for row in rows
        if "postgres" in row["body"].lower() and "indexing" in row["body"].lower()
    ]
    assert len(hits) >= 1000
    assert any("Postgres Indexing" in row["title"] for row in hits)


@pytest.mark.docker
def test_document_corpus_has_postgresql_tsquery_hits() -> None:
    try:
        with psycopg.connect(content_seed.database_url(), connect_timeout=1) as connection:
            connection.execute("SELECT 1")
    except psycopg.OperationalError as exc:
        pytest.skip(f"PostgreSQL lab is not reachable: {exc}")

    plan = content_seed.plan_seed("document_search", phase="8")
    content_seed.execute_seed(plan, reset=True, generate=True)

    with psycopg.connect(content_seed.database_url(), connect_timeout=1) as connection:
        count = connection.execute(
            """
            SELECT count(*)
            FROM documents.docs
            WHERE search_vec @@ websearch_to_tsquery('english', 'postgres indexing')
            """
        ).fetchone()[0]
        plan_text = "\n".join(
            row[0]
            for row in connection.execute(
                """
                EXPLAIN
                SELECT count(*)
                FROM documents.docs
                WHERE search_vec @@ websearch_to_tsquery('english', 'postgres indexing')
                """
            )
        )

    assert count >= 1000
    assert "docs_search_vec_gin_idx" in plan_text
