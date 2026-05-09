# Repo State

Current baseline:

- Python package: `src/pgfound/`
- CLI entry point: `pgfound = pgfound.cli:main`
- CLI surface: `pgfound version`, `doctor`, `lab`, `content`, `exercise`,
  `progress`, `review`, `decision`, and `interview` command groups.
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
- Phase 0 corpus: PROMPT_10 added the full reality-before-syntax paper
  modeling content set: 10 active lessons, 40 modeling exercises, Phase 0
  lesson/exercise pointer READMEs, the default paper-modeling rubric, domain
  README Phase 0 notes, validator phase overrides for paper exercises, and
  phase-corpus tests.
- Phase 1 corpus and runner: PROMPT_11 added the full SQL literacy basics
  content set: 10 active lessons, 70 active SQL exercises, Phase 1
  lesson/exercise pointer READMEs, `pgfound exercise run`, dry-run and
  answer-check modes, progress scaffolding under `tmp/progress/`, and Phase 1
  corpus/runner tests.
- Phase 2 corpus and row-set checking: PROMPT_12 added the relational joins
  and aggregation content set: 8 active lessons, 56 active SQL exercises,
  Phase 2 lesson/exercise pointer READMEs, seed extensions for ecommerce,
  scheduling, and SaaS multi-tenancy, `output_comparison` modes for exercise
  checking, and Phase 2 corpus tests.
- Phase 3 corpus and schema-object checking: PROMPT_13 added the schema design
  and database-enforced truth content set: 12 active lessons, 68 schema and
  critique exercises, Phase 3 lesson/exercise pointer READMEs, constraint and
  reference-table seed extensions for ecommerce, scheduling, and SaaS
  multi-tenancy, a legacy ecommerce spreadsheet fixture, `schema_object`
  exercise checking via `information_schema`, `docs/constraints-cookbook.md`,
  and Phase 3 corpus tests.
- Seed and runner polish: PROMPT_14 added `pgfound content seed-doctor`,
  per-exercise `search_path`, canonical `tmp/progress/exercises/*.json`
  attempt records, `pgfound progress show`, exercise runner `--answer`,
  `--no-prompt`, and `--save-answer`, plus `pgfound lab reset-domain`,
  `snapshot`, and `restore`.

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
- `docs/constraints-cookbook.md`
- `docs/learner-workflow.md`
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
- `uv run pgfound content seed ecommerce --phase 3 --reset`
- `uv run pgfound content seed scheduling --phase 3 --reset`
- `uv run pgfound content seed saas_multi_tenant --phase 3 --reset`
- `uv run pgfound content validate --include-examples`
- `uv run pgfound content seed-doctor`
- `uv run pgfound exercise run first-select-write-query --dry-run`
- `uv run pgfound progress show`
- `docker compose -f docker/docker-compose.yml config`

Known local-only artifacts may exist after verification: `.venv/`,
`.pytest_cache/`, `.ruff_cache/`, and `__pycache__/`. They are ignored.
