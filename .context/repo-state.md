# Repo State

Current baseline:

- Python package: `src/pgfound/`
- CLI entry point: `pgfound = pgfound.cli:main`
- Test suite: `tests/test_smoke.py`
- Tooling: `uv`, `ruff`, `pytest`
- Docs state: PROMPT_02 added doctrine, architecture, repo layout, LLM usage,
  and ADR infrastructure under `docs/`.
- Docker lab: PROMPT_03 added a Docker Compose PostgreSQL 16 lab under
  `docker/`, init SQL scripts, a sandbox profile, Makefile lab targets, and
  `docs/lab.md`.

Canonical docs:

- `docs/doctrine.md`
- `docs/architecture.md`
- `docs/repo-layout.md`
- `docs/llm-usage.md`
- `docs/lab.md`
- `docs/adr/README.md`
- `docs/adr/template.md`

Expected green checks:

- `uv sync`
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run pytest -q`
- `uv run pgfound`
- `docker compose -f docker/docker-compose.yml config`

Known local-only artifacts may exist after verification: `.venv/`,
`.pytest_cache/`, `.ruff_cache/`, and `__pycache__/`. They are ignored.
