# Python uv Ruff Pytest Toolchain

## Status

Accepted

## Date

2026-05-07

## Context

The repository needs a small, dependable Python toolchain for command-line
support, validation, tests, and future content checks. The project should be
easy to bootstrap on macOS and Linux, and it should avoid multiple competing
dependency manifests. The first scaffold already established a Python package
under `src/pgfound/`, a CLI entry point, `pyproject.toml`, `uv.lock`, Ruff, and
pytest.

## Decision

Use `uv` for Python environment and dependency management, Ruff for formatting
and linting, and pytest for automated tests. `pyproject.toml` is the project
configuration surface, and `uv.lock` records the resolved environment. The
repository will not add `requirements.txt`.

## Consequences

Bootstrap and verification stay concise: `uv sync`, `uv run ruff check .`,
`uv run ruff format --check .`, and `uv run pytest -q`. The lockfile makes
local and CI behavior easier to reproduce. Contributors need `uv`, but they do
not need to manage virtual environments manually. Python automation should
follow this toolchain unless a later ADR changes it.

## Alternatives considered

Plain `pip` with `requirements.txt` was rejected because it creates a second
dependency surface and weaker environment reproducibility. Poetry was not
chosen because `uv` provides a faster, simpler path for this repository's early
needs. Separate formatters and linters were rejected in favor of Ruff's unified
workflow.

## Related ADRs/docs

- [Doctrine](../doctrine.md)
- [Repo layout](../repo-layout.md)
