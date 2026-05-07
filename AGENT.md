# Agent Guide

This repository is `postgres-foundations`: a PostgreSQL training lab,
assessment system, design studio, and planning engine. Keep the implementation
concrete, operational, and PostgreSQL core-first.

## Operating Rules

- Treat `.prompts/` as the authoritative build sequence. Prompts are monotonic:
  run only the prompt the user names, verify prior state, and do not advance to
  the next prompt unless explicitly asked.
- Preserve user notes and unrelated work. In particular, leave
  `human-notes.md` alone unless the user directly asks to edit it.
- Prefer small, reviewable changes that match the current prompt. Do not author
  curriculum, Docker, decision-engine data, or doctrine files before their
  prompt asks for them.
- Use `uv` for Python environment management. Do not add `requirements.txt`.
- Use `ruff` for lint/format and `pytest` for tests.

## Doctrine Snapshot

- PostgreSQL core first; extensions require real workload signals.
- "Not yet" is a valid recommendation when capability would add premature
  operational burden.
- Every recommendation should be explainable, operationally aware, and
  portability-conscious.
- This is not a blog, video course, or generic LMS. It is an implementation
  lab with assessment, review, design practice, and planning support.

## Current Commands

- Install: `uv sync`
- Format: `uv run ruff format .`
- Lint: `uv run ruff check .`
- Test: `uv run pytest -q`
- CLI smoke: `uv run pgfound`

## Context Files

Use `.context/` for short, agent-facing references that can be updated as the
promptset creates real project artifacts:

- `.context/repo-state.md` records the current scaffold and verification state.
- `.context/prompt-log.md` tracks completed prompts and the next expected prompt.
- `.context/runbooks/prompt-execution.md` captures the normal prompt, review,
  fix, and commit workflow.
- `.context/indexes/README.md` points to canonical docs/catalogs as they appear.

When a later prompt creates canonical documentation under `docs/` or structured
data under `decision-engine/`, update `.context/` to link to it rather than
copying full content.
