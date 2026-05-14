# CI Requirements

The integration suite expects the standard Python toolchain from the repository:

- `uv sync`
- `uv run ruff check .`
- `uv run pytest`
- `make test-integration`

Docker is required for tests marked with `@pytest.mark.docker`. The default CI
environment should provide the plain PostgreSQL lab profile (`pg`) so database
integration checks can run against core PostgreSQL behavior.

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
