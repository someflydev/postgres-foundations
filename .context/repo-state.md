# Repo State

Current baseline:

- Python package: `src/pgfound/`
- CLI entry point: `pgfound = pgfound.cli:main`
- Test suite: `tests/test_smoke.py`
- Tooling: `uv`, `ruff`, `pytest`
- Docs state: `docs/` and `docs/adr/` are intentionally empty except
  `.gitkeep` until PROMPT_02.

Expected green checks:

- `uv sync`
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run pytest -q`
- `uv run pgfound`

Known local-only artifacts may exist after verification: `.venv/`,
`.pytest_cache/`, `.ruff_cache/`, and `__pycache__/`. They are ignored.
