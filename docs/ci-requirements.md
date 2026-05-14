# CI Requirements

The default CI suite expects the standard Python toolchain from the repository:

- `uv sync`
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run pgfound content validate --strict`
- `uv run pgfound content lint --strict`
- `uv run pgfound decision catalog check`
- `uv run pgfound decision rules lint`
- `uv run pgfound docs check`
- `uv run pytest`
- `uv run pgfound decision golden-refresh --dry-run`

Docker is required for tests marked with `@pytest.mark.docker`. The default CI
environment provides a plain PostgreSQL 16 service so core database integration
checks can run without requiring local Compose extension profiles.

Optional extension profiles are not required in default CI:

- PostGIS
- pgvector
- TimescaleDB
- Citus
- pg_partman
- PgBouncer
- HBA overlay
- replication

Tests that require one of those profiles must mark that requirement explicitly
and skip when the profile is not available. Default CI only treats the plain
`pg` profile as mandatory.
