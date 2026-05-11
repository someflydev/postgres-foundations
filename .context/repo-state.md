# Repo State

Current baseline:

- Python package: `src/pgfound/`
- CLI entry point: `pgfound = pgfound.cli:main`
- CLI surface: `pgfound version`, `doctor`, `lab`, `content`, `exercise`,
  `capstone`, `progress`, `review`, `decision`, and `interview` command
  groups.
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
- Phase 4a PostgreSQL data modeling: PROMPT_15 added the timestamps/time
  zones, UUID, and JSON/JSONB content set: 9 active lessons, 63 active
  exercises, Phase 4a seed extensions for ecommerce, scheduling, and SaaS
  multi-tenancy, `docs/anti-patterns/jsonb_everything.md`, JSON-aware rowset
  comparison, a `multi_session_trace` comparator placeholder, and Phase 4a
  corpus tests.
- Phase 4b PostgreSQL data modeling: PROMPT_16 added arrays, ranges, and
  multiranges: 10 active lessons, 70 active exercises, Phase 4b seed
  extensions for ecommerce, scheduling, and event-heavy ops,
  `docs/anti-patterns/arrays_over_child_tables.md`, exclusion-constraint
  cookbook guidance, array/range comparison normalization, and Phase 4b corpus
  tests.
- Phase 5 expressive querying: PROMPT_17 added CTE, recursive CTE, window
  function, lateral join, upsert, EXISTS/NOT EXISTS, view, materialized view,
  and synthesis content: 12 active lessons, 96 active exercises, Phase 5 seed
  extensions for ecommerce, scheduling, SaaS multi-tenancy, and event-heavy
  ops, `docs/expressive-sql-style.md`, glossary additions, ordered-output
  authoring guidance, exercise-runner `--timing`, and Phase 5 corpus tests.
- Phase 6 transactions, concurrency, and correctness: PROMPT_18 added
  transaction, MVCC, isolation, race, lock, deadlock, and idempotency content:
  12 active lessons, 96 active exercises, Phase 6 seed extensions for
  ecommerce and scheduling, a small `bank` mini-domain for transfer drills,
  multi-session exercise metadata (`sessions`, `lab_harness_profile`),
  scaffold support for `--sessions`, `docs/concurrency-playbook.md`, glossary
  additions, and Phase 6 corpus tests.
- Multi-session concurrency harness: PROMPT_19 added
  `src/pgfound/lab/harness.py`, `pgfound lab concurrency list|run|record`,
  scenario YAML files under `scenarios/concurrency/`, exercise `--check`
  integration for `multi_session_trace`, and `docs/concurrency-harness.md`.
- Phase 7a indexing fundamentals: PROMPT_20 added scans, EXPLAIN basics,
  B-tree, composite indexes, covering indexes, and index-cost content: 8 active
  lessons, 64 active exercises, Phase 7a generated ecommerce/scheduling seed
  extensions, `pgfound lab explain`, `docs/indexing-playbook-part1.md`,
  `docs/observability-intro.md`, glossary additions, and Phase 7a corpus tests.
- Phase 7b advanced indexing: PROMPT_21 added partial, expression, GIN, GiST,
  BRIN, deep EXPLAIN, estimated-vs-actual, and extended-statistics content:
  10 active lessons, 80 active exercises, Phase 7b ecommerce/event seed
  extensions, `docs/indexing-playbook-part2.md`, unused/redundant index
  anti-pattern docs, and fixture-based explain diff tests.
- Phase 8 PostgreSQL full-text search: PROMPT_22 added lexical search content:
  10 active lessons, 80 active exercises, a 5000-row `document_search` FTS
  corpus with generated `tsvector` and GIN index, ecommerce product search
  vectors, `unaccent` lab initialization, pg_trgm/pgvector forward pointers,
  `docs/search-playbook.md`, and Phase 8 corpus tests.
- Phase 9 partitioning and large-table operations: PROMPT_23 added
  partitioning content: 10 active lessons, 80 active exercises,
  `events.event_log_partitioned` with monthly range partitions, parent BRIN and
  B-tree partitioned indexes, a detached cold-partition retention example,
  `ecommerce.orders_partitioned` with quarterly range partitions for
  comparison, deterministic Phase 9 partition metadata generation,
  `docs/partitioning-playbook.md`, `docs/anti-patterns/partition_too_early.md`,
  partitioned-table index guidance in `docs/indexing-playbook-part2.md`, and
  Phase 9 corpus/seed tests.
- Phase 10 roles, RLS, replication, and FDW: PROMPT_24 added security and
  federation content: 12 active lessons, 96 active exercises, SaaS document and
  audit tables protected by tenant-scoped RLS policies, a modernization
  loopback `postgres_fdw` bridge, a `replication` Docker profile with
  `pg-replica`, `docs/rls-playbook.md`,
  `docs/logical-replication-playbook.md`, glossary additions, and Phase 10
  corpus/RLS policy tests.
- Capstones 1 and 2: PROMPT_25 added `capstones/01-multi-tenant-saas-crm/`
  and `capstones/02-scheduling-availability/` with learner starter files,
  reference DDL/query/runbook/writeup material, composed capstone rubrics,
  `pgfound capstone start|evaluate`, and a scheduling double-booking scenario
  under `scenarios/concurrency/`.
- Capstones 3 and 4: PROMPT_26 added `capstones/03-event-heavy-ops/` and
  `capstones/04-modernization-bridge/` with learner starter files, reference
  DDL/query/runbook/writeup material, event retention and FDW wiring scripts,
  extension-posture and operational-reasoning rubric dimensions, a capstones
  README, a stale materialized-view FDW concurrency scenario, and a Phase 10
  critique exercise for the modernization bridge.

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
- `docs/anti-patterns/jsonb_everything.md`
- `docs/anti-patterns/arrays_over_child_tables.md`
- `docs/expressive-sql-style.md`
- `docs/concurrency-playbook.md`
- `docs/concurrency-harness.md`
- `docs/indexing-playbook-part1.md`
- `docs/indexing-playbook-part2.md`
- `docs/observability-intro.md`
- `docs/anti-patterns/unused_indexes.md`
- `docs/anti-patterns/redundant_indexes.md`
- `docs/search-playbook.md`
- `docs/partitioning-playbook.md`
- `docs/rls-playbook.md`
- `docs/logical-replication-playbook.md`
- `docs/anti-patterns/partition_too_early.md`
- `capstones/README.md`
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
- `uv run pgfound content seed ecommerce --phase 4a --reset`
- `uv run pgfound content seed scheduling --phase 4a --reset`
- `uv run pgfound content seed saas_multi_tenant --phase 4a --reset`
- `uv run pgfound content seed ecommerce --phase 4b --reset`
- `uv run pgfound content seed scheduling --phase 4b --reset`
- `uv run pgfound content seed event_heavy_ops --phase 4b --reset`
- `uv run pgfound content seed ecommerce --phase 5 --reset`
- `uv run pgfound content seed scheduling --phase 5 --reset`
- `uv run pgfound content seed saas_multi_tenant --phase 5 --reset`
- `uv run pgfound content seed event_heavy_ops --phase 5 --reset`
- `uv run pgfound content seed ecommerce --phase 6 --reset`
- `uv run pgfound content seed scheduling --phase 6 --reset`
- `uv run pgfound content seed ecommerce --phase 7a --reset --generate`
- `uv run pgfound content seed scheduling --phase 7a --reset --generate`
- `uv run pgfound content seed ecommerce --phase 7b --reset --generate`
- `uv run pgfound content seed event_heavy_ops --phase 7b --reset`
- `uv run pgfound content seed document_search --phase 8 --reset --generate`
- `uv run pgfound content seed ecommerce --phase 8 --reset --generate`
- `uv run pgfound content seed event_heavy_ops --phase 9 --reset --generate`
- `uv run pgfound content seed ecommerce --phase 9 --reset --generate`
- `uv run pgfound content seed saas_multi_tenant --phase 10 --reset`
- `uv run pgfound content seed modernization_bridge --phase 10 --reset`
- `uv run pgfound exercise run what-lateral-unlocks-level-c-1 --check --answer exercises/phase-05-expressive-querying/what-lateral-unlocks/level-c/what-lateral-unlocks-level-c-1/solution.sql --no-prompt --timing`
- `uv run pgfound content validate --include-examples`
- `uv run pgfound content seed-doctor`
- `uv run pgfound exercise run first-select-write-query --dry-run`
- `uv run pgfound lab concurrency run scenarios/concurrency/inventory-lost-update.yaml`
- `uv run pgfound capstone start 03-event-heavy-ops`
- `uv run pgfound capstone start 04-modernization-bridge`
- `uv run pgfound lab explain --help`
- `uv run pytest -q -m 'not docker'`
- `uv run pgfound progress show`
- `docker compose -f docker/docker-compose.yml config`

Known local-only artifacts may exist after verification: `.venv/`,
`.pytest_cache/`, `.ruff_cache/`, and `__pycache__/`. They are ignored.
