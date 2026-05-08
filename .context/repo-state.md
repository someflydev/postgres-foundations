# Repo State

Current baseline:

- Python package: `src/pgfound/`
- CLI entry point: `pgfound = pgfound.cli:main`
- CLI surface: `pgfound version`, `doctor`, `lab`, `content`, `review`,
  `decision`, and `interview` command groups.
- Test suite: `tests/test_cli.py`, `tests/test_paths.py`,
  `tests/test_lab_psql.py`, and Docker Compose tests.
- Tooling: `uv`, `ruff`, `pytest`
- Docs state: PROMPT_02 added doctrine, architecture, repo layout, LLM usage,
  and ADR infrastructure under `docs/`.
- Docker lab: PROMPT_03 added a Docker Compose PostgreSQL 16 lab under
  `docker/`, init SQL scripts, a sandbox profile, Makefile lab targets, and
  `docs/lab.md`.
- Platform package: PROMPT_04 added config/path helpers, placeholder content
  dataclasses/loaders, Docker Compose wrappers, psql argv building, review and
  decision scaffolds, and `docs/cli.md`.
- Content validation: PROMPT_05 added draft 2020-12 JSON Schemas under
  `content-schemas/`, one valid example per kind under
  `content-schemas/examples/`, and a real `pgfound content validate` command
  with schema validation, YAML loading, cross-file checks, `--paths`,
  `--strict`, and `--include-examples`.
- Curriculum map: PROMPT_06 added `curriculum/map.json`, human-readable
  curriculum docs under `curriculum/`, `docs/glossary.md`,
  `content-schemas/curriculum.schema.json`, and default validation for the
  curriculum map.
- Lesson authoring: PROMPT_07 added root `lessons/` phase directories,
  lesson templates under `content-schemas/templates/`, `pgfound content
  scaffold lesson`, `pgfound content lint`, lesson-specific validator checks,
  and `docs/authoring-lessons.md`.
- Exercise authoring: PROMPT_08 added root `exercises/` authoring directories,
  `pgfound content scaffold exercise`, exercise level validation,
  forbidden-concept SQL lint, default rubrics under `rubrics/default/`, and
  `docs/authoring-exercises.md`.
- Reusable domains: PROMPT_09 added seed packs under `seed-data/packs/` for
  ecommerce, scheduling, SaaS multi-tenancy, event-heavy operations, document
  search, and modernization bridge; `pgfound content seed`; domain manifest
  validation; deterministic CSV generator tests; and
  `docs/domain-conventions.md`.

Canonical docs:

- `docs/doctrine.md`
- `docs/architecture.md`
- `docs/repo-layout.md`
- `docs/llm-usage.md`
- `docs/lab.md`
- `docs/cli.md`
- `docs/authoring.md`
- `docs/authoring-lessons.md`
- `docs/authoring-exercises.md`
- `docs/domain-conventions.md`
- `docs/glossary.md`
- `curriculum/README.md`
- `curriculum/capability-layers.md`
- `curriculum/domains.md`
- `docs/adr/README.md`
- `docs/adr/template.md`

Expected green checks:

- `uv sync`
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run pytest -q`
- `uv run pgfound --help`
- `uv run pgfound doctor`
- `uv run pgfound content list`
- `uv run pgfound content validate`
- `uv run pgfound content lint`
- `uv run pgfound content validate --include-examples`
- `docker compose -f docker/docker-compose.yml config`

Known local-only artifacts may exist after verification: `.venv/`,
`.pytest_cache/`, `.ruff_cache/`, and `__pycache__/`. They are ignored.
