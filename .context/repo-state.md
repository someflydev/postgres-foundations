# Repo State

Current baseline:

- Python package: `src/pgfound/`
- CLI entry point: `pgfound = pgfound.cli:main`
- CLI surface: `pgfound version`, `doctor`, `lab`, `ops`, `content`, `exercise`,
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
- Decision engine architecture: PROMPT_39 replaced the decision stub with
  `pgfound decision run <intake.json>`, added decision-engine schemas,
  architecture docs, intake fixtures, JSON/Markdown report writing, and tests
  for empty-but-valid reports while catalogs/rules are pending.
- Decision engine catalogs: PROMPT_40 added authored catalogs for industries,
  data shapes, and workload patterns under `decision-engine/catalogs/`,
  upgraded their schemas to full entry validation, and added
  `pgfound decision catalog list|check` with cross-catalog integrity checks.
- Decision engine catalog completion: PROMPT_41 added authored catalogs for
  PostgreSQL core features, extensions and operational tools, index patterns,
  topology patterns, and anti-patterns; expanded their schemas to full entry
  validation; added explicit extension not-yet trigger requirements plus
  extension/index/topology/module/doc cross-link checks; and added
  `docs/extension-catalog-sync.md`.
- Decision engine rules: PROMPT_42 replaced the placeholder rule schema with
  declarative rules, added `decision-engine/rules/` authoring docs and 40+
  active rule files, implemented rule matching/aggregation/linting under
  `src/pgfound/decision/`, added `pgfound decision rules lint`, `decision run
  --rules`, and `--explain`, and generated golden fixture reports under
  `decision-engine/fixtures/reports/`.
- Decision engine scoring/reporting: PROMPT_43 added configurable weighted
  scoring via `decision-engine/scoring-weights.json`, per-recommendation score
  breakdowns and class rollups, score-based verdict downgrades, grouped
  follow-up questions, Jinja2 Markdown report templates, `decision run
  --format json|markdown|both`, `--show-scores`, `decision diff`, tokenized
  free-form note matching, a guarded golden regeneration script, and
  `docs/decision-engine-usage.md`.
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
- Review engine: PROMPT_27 added `pgfound exercise review`, implemented
  `pgfound capstone evaluate` and `pgfound review run`, introduced
  `src/pgfound/review/` result models, grading, runners, Markdown/JSON output,
  plan diffing, sandbox-backed `--full` capstone SQL/query checks, rubric
  `signals`, capstone writeup/critical-query metadata, and
  `docs/review-engine.md` plus `docs/rubric-signals.md`.
- Interview simulator: PROMPT_28 added `src/pgfound/interview/`,
  `pgfound interview start|review`, strict transcript files under
  `tmp/interviews/`, prompt templates under `llm-prompts/interview/stages/`,
  interview rubrics under `rubrics/interview/`, six initial interview
  scenarios under `scenarios/interviews/`, a dedicated
  `content-schemas/interview-scenario.schema.json`, and
  `docs/interview-simulator.md`.
  The interview stage templates are stub templates without PROMPT_29 front
  matter; future LLM-template validation should treat them as interview-stage
  assets until PROMPT_30 replaces or upgrades them.
- Training-side LLM prompt templates: PROMPT_29 added front-matter Markdown
  templates under `llm-prompts/coaching/`, `llm-prompts/critique/`,
  `llm-prompts/remediation/`, and `llm-prompts/shared/`; documented the
  template format in `llm-prompts/template-format.md`; added Jinja2-backed
  rendering in `src/pgfound/llm/`; added `pgfound llm list|render`; and writes
  LLM prompt artifacts from `exercise review --full` and capstone full
  evaluation.
- Interview and capstone reviewer LLM prompts: PROMPT_30 added
  `llm-prompts/interview/personas/`, upgraded interview stage prompts to the
  YAML-front-matter/Jinja2 format, added follow-up and closing-feedback prompt
  rendering, added `pgfound interview dispatch`, and added capstone reviewer
  prompt bundles under `tmp/reviews/capstone/<id>/<timestamp>/`.
- Administration track A1-A2: PROMPT_31 added `curriculum/admin/map.json`
  with A1-A6 module anchors, validator/schema support for `admin_map` content
  and admin lesson `module_id` directory checks, 15 active lessons under
  `lessons/admin/`, 120 exercises under `exercises/admin/`, admin role/access
  review SQL under `seed-data/packs/admin/`, `docs/admin-track/`, and admin
  corpus/map tests.
- Administration track A3-A4: PROMPT_32 added auth/pooling and
  backup/maintenance/lifecycle content: 17 active lessons under
  `lessons/admin/a3-auth-and-pooling/` and
  `lessons/admin/a4-maintenance-and-lifecycle/`, 136 exercises under matching
  `exercises/admin/` modules, optional `restore_drill` exercise metadata,
  `docker/hba_overlay/`, `docker/pgbouncer/`, HBA overlay and PgBouncer Compose
  profiles, `scripts/restore-drill.sh`, A3/A4 admin playbooks, and admin
  A3/A4 plus PgBouncer compose tests.
- Administration track A5-A6: PROMPT_33 added monitoring/performance and
  replication/HA operations content: 17 active lessons under
  `lessons/admin/a5-monitoring-and-performance-ops/` and
  `lessons/admin/a6-replication-and-ha/`, 136 exercises under matching
  `exercises/admin/` modules, canonical SQL scripts under
  `scripts/monitoring/`, `pgfound ops query <name>`,
  `docs/admin-track/a5-monitoring-playbook.md`,
  `docs/admin-track/a6-replication-ha-playbook.md`,
  `docs/postmortem-template.md`, and admin A5/A6 plus ops query tests.
- Extension track E1-E2: PROMPT_34 added
  `curriculum/extensions/map.json` with E1-E7 anchors (`pg_stat_statements`,
  `pg_trgm`, PostGIS, pgvector, TimescaleDB, postgres_fdw, pg_cron), plus
  ltree, pg_partman, and PgBouncer; validator/schema support for the
  extension map and extension lesson `module_id` directory checks; 13 active lessons under
  `lessons/extensions/e1-pg-stat-statements/` and
  `lessons/extensions/e2-pg-trgm/`; 104 exercises under matching
  `exercises/extensions/` modules; `docs/extension-track/`; a pg_trgm pointer
  in `docs/search-playbook.md`; `CREATE EXTENSION IF NOT EXISTS pg_trgm;` in
  `docker/initdb/00-extensions.sql`; and extension map/corpus tests.
- Extension track E3-E4: PROMPT_35 added optional PostGIS and pgvector Docker
  Compose profiles while keeping the main `pg` service on plain
  `postgres:16`; doctor now reports those profile definitions; 10 PostGIS
  lessons and 80 exercises under `lessons/extensions/e3-postgis/` and
  `exercises/extensions/e3-postgis/`; 9 pgvector lessons and 72 exercises
  under `lessons/extensions/e4-pgvector/` and
  `exercises/extensions/e4-pgvector/`; `seed-data/packs/logistics_geo/` with
  checked-in GeoJSON service zones loaded through `ST_GeomFromGeoJSON`; optional
  deterministic fake embeddings in `document_search` phase 08 when `vector` is
  available; E3/E4 extension docs; geo/vector anti-pattern docs; and
  PostGIS/pgvector profile plus E3/E4 corpus tests.
- Extension track E5-E6: PROMPT_36 added an optional TimescaleDB Docker Compose
  profile on port 5438 using `timescale/timescaledb:2.15.3-pg16` and a
  Timescale-specific init script while keeping the main `pg` service plain;
  doctor now reports the Timescale profile definition; 9 TimescaleDB lessons
  and 72 exercises under `lessons/extensions/e5-timescaledb/` and
  `exercises/extensions/e5-timescaledb/`; 8 deep postgres_fdw lessons and 64
  exercises under `lessons/extensions/e6-postgres-fdw/` and
  `exercises/extensions/e6-postgres-fdw/`; E5/E6 extension docs; the
  `timescale_too_early` anti-pattern referencing Phase 9 partitioning; and
  Timescale profile plus E5/E6 corpus tests.
- Extension track E7 and remaining modules: PROMPT_37 replaced the old
  `e7-pg-cron` placeholder with `e7-citus`; added a Citus Compose profile
  (`citusdata/citus:12.1`) with a coordinator on port 5439, two workers, and
  Citus-specific coordinator/worker init directories;
  added a `pgpartman` profile backed by `docker/pg-with-partman/Dockerfile`
  on port 5440; extended doctor profile checks; authored 26 active lessons
  and 208 exercises across `lessons/extensions/e7-citus/`,
  `lessons/extensions/ltree/`, `lessons/extensions/pg-partman/`, and
  `lessons/extensions/pgbouncer/`; added corresponding extension docs and the
  `shard_without_distribution_key` anti-pattern; and added Citus/profile plus
  E7/misc corpus tests.
- Extension-oriented capstones: PROMPT_38 added capstones
  `05-geo-logistics-platform`, `06-ai-knowledge-platform`,
  `07-observability-event-analytics`, and
  `08-modernization-bridge-extensions` with starter/reference layouts,
  composed rubrics, extension-posture-heavy assessment, critical queries,
  operational runbooks, and 2500-3500 word reference writeups. It also added
  deterministic capstone posture signals for insufficient PostGIS
  justification, pgvector without lexical baseline, Citus without
  distribution-key justification, and TimescaleDB without partitioning
  comparison; these feed the extension-posture rubric and are documented in
  `docs/capstone-posture-signals.md`.

Canonical docs:

- `docs/doctrine.md`
- `docs/architecture.md`
- `docs/repo-layout.md`
- `docs/llm-usage.md`
- `docs/llm-integration.md`
- `docs/llm-provider-neutrality.md`
- `docs/lab.md`
- `docs/cli.md`
- `docs/review-engine.md`
- `docs/rubric-signals.md`
- `docs/capstone-posture-signals.md`
- `docs/interview-simulator.md`
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
- `docs/admin-track/README.md`
- `docs/admin-track/a1-roles-playbook.md`
- `docs/admin-track/a2-schemas-playbook.md`
- `docs/admin-track/a3-auth-and-pooling-playbook.md`
- `docs/admin-track/a4-backup-and-upgrades-playbook.md`
- `docs/admin-track/a5-monitoring-playbook.md`
- `docs/admin-track/a6-replication-ha-playbook.md`
- `docs/postmortem-template.md`
- `docs/extension-track/README.md`
- `docs/extension-track/e1-pg-stat-statements.md`
- `docs/extension-track/e2-pg-trgm.md`
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
- `uv run pgfound decision catalog check`
- `uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json`
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
