# Context Indexes

This directory holds short indexes to canonical project artifacts as they are
created by prompts.

Canonical docs introduced by PROMPT_02:

- `docs/doctrine.md`
- `docs/architecture.md`
- `docs/repo-layout.md`
- `docs/llm-usage.md`
- `docs/adr/README.md`
- `docs/adr/template.md`
- `docs/adr/0001-python-uv-ruff-pytest-toolchain.md`
- `docs/adr/0002-json-first-content-model.md`
- `docs/adr/0003-docker-for-the-lab.md`
- `docs/adr/0004-core-first-extension-doctrine.md`
- `docs/adr/0005-decision-engine-is-explainable.md`

Docker lab references introduced by PROMPT_03:

- `docs/lab.md`
- `docker/docker-compose.yml`
- `docker/initdb/`
- `docker/postgresql.conf.d/README.md`

CLI references introduced by PROMPT_04:

- `docs/cli.md`
- `src/pgfound/cli.py`

Content schema references introduced by PROMPT_05:

- `content-schemas/common.json`
- `content-schemas/*.schema.json`
- `content-schemas/examples/*.example.json`
- `docs/authoring.md`
- `src/pgfound/content/validate.py`

Curriculum references introduced by PROMPT_06:

- `curriculum/map.json`
- `curriculum/README.md`
- `curriculum/capability-layers.md`
- `curriculum/domains.md`
- `docs/glossary.md`
- `content-schemas/curriculum.schema.json`

Lesson authoring references introduced by PROMPT_07:

- `lessons/phase-*/`
- `content-schemas/templates/lesson.json.template`
- `content-schemas/templates/lesson-body.md.template`
- `docs/authoring-lessons.md`
- `src/pgfound/content/scaffold.py`
- `src/pgfound/content/lint.py`

Exercise authoring references introduced by PROMPT_08:

- `exercises/phase-*/`
- `rubrics/default/*.rubric.json`
- `docs/authoring-exercises.md`
- `src/pgfound/content/scaffold.py`
- `src/pgfound/content/validate.py`
- `src/pgfound/content/lint.py`

Reusable domain references introduced by PROMPT_09:

- `seed-data/packs/*/manifest.json`
- `seed-data/packs/*/README.md`
- `seed-data/packs/*/phases/phase-*.sql`
- `seed-data/packs/*/generators/*.py`
- `docs/domain-conventions.md`
- `content-schemas/manifest.schema.json`
- `src/pgfound/content/seed.py`
- `docs/cli.md`

Phase 0 paper-modeling references introduced by PROMPT_10:

- `lessons/phase-00-reality-before-syntax/README.md`
- `exercises/phase-00-reality-before-syntax/README.md`
- `rubrics/default/paper-modeling.rubric.json`
- `content-schemas/phase-exercise-overrides.schema.json`
- `docs/authoring-exercises.md`
- `tests/test_phase0_corpus.py`

Phase 1 SQL literacy references introduced by PROMPT_11:

- `lessons/phase-01-sql-literacy-basics/README.md`
- `exercises/phase-01-sql-literacy-basics/README.md`
- `src/pgfound/exercise.py`
- `docs/cli.md`
- `tests/test_phase1_corpus.py`
- `tests/test_exercise_run_dry_run.py`

Phase 2 relational joins references introduced by PROMPT_12:

- `lessons/phase-02-relational-joins-and-aggregation/README.md`
- `exercises/phase-02-relational-joins-and-aggregation/README.md`
- `seed-data/packs/ecommerce/phases/phase-02.sql`
- `seed-data/packs/scheduling/phases/phase-02.sql`
- `seed-data/packs/saas_multi_tenant/phases/phase-02.sql`
- `src/pgfound/exercise.py`
- `tests/test_phase2_corpus.py`

Phase 3 database-truth references introduced by PROMPT_13:

- `lessons/phase-03-schema-design-and-database-truth/README.md`
- `exercises/phase-03-schema-design-and-database-truth/README.md`
- `seed-data/packs/ecommerce/phases/phase-03.sql`
- `seed-data/packs/ecommerce/fixtures/spreadsheet-legacy.csv`
- `seed-data/packs/scheduling/phases/phase-03.sql`
- `seed-data/packs/saas_multi_tenant/phases/phase-03.sql`
- `docs/constraints-cookbook.md`
- `src/pgfound/exercise.py`
- `tests/test_phase3_corpus.py`

Seed and runner polish references introduced by PROMPT_14:

- `src/pgfound/content/seed_doctor.py`
- `src/pgfound/progress.py`
- `src/pgfound/lab/psql.py`
- `docs/learner-workflow.md`

Phase 4a PostgreSQL data modeling references introduced by PROMPT_15:

- `lessons/phase-04-postgresql-data-modeling/`
- `exercises/phase-04-postgresql-data-modeling/`
- `seed-data/packs/ecommerce/phases/phase-04a.sql`
- `seed-data/packs/scheduling/phases/phase-04a.sql`
- `seed-data/packs/saas_multi_tenant/phases/phase-04a.sql`
- `docs/anti-patterns/jsonb_everything.md`
- `src/pgfound/exercise.py`
- `tests/test_phase4a_corpus.py`

Phase 4b PostgreSQL data modeling references introduced by PROMPT_16:

- `lessons/phase-04-postgresql-data-modeling/`
- `exercises/phase-04-postgresql-data-modeling/`
- `seed-data/packs/ecommerce/phases/phase-04b.sql`
- `seed-data/packs/scheduling/phases/phase-04b.sql`
- `seed-data/packs/event_heavy_ops/phases/phase-04b.sql`
- `docs/anti-patterns/arrays_over_child_tables.md`
- `docs/constraints-cookbook.md`
- `src/pgfound/exercise.py`
- `tests/test_phase4b_corpus.py`

Phase 5 expressive querying references introduced by PROMPT_17:

- `lessons/phase-05-expressive-querying/`
- `exercises/phase-05-expressive-querying/`
- `seed-data/packs/ecommerce/phases/phase-05.sql`
- `seed-data/packs/scheduling/phases/phase-05.sql`
- `seed-data/packs/saas_multi_tenant/phases/phase-05.sql`
- `seed-data/packs/event_heavy_ops/phases/phase-05.sql`
- `docs/expressive-sql-style.md`
- `docs/glossary.md`
- `docs/authoring-exercises.md`
- `src/pgfound/exercise.py`
- `src/pgfound/content/seed_doctor.py`
- `tests/test_phase5_corpus.py`

Phase 6 transactions/concurrency references introduced by PROMPT_18:

- `lessons/phase-06-transactions-concurrency-and-correctness/`
- `exercises/phase-06-transactions-concurrency-and-correctness/`
- `seed-data/packs/ecommerce/phases/phase-06.sql`
- `seed-data/packs/scheduling/phases/phase-06.sql`
- `docs/concurrency-playbook.md`
- `docs/glossary.md`
- `docs/authoring-exercises.md`
- `content-schemas/exercise.schema.json`
- `src/pgfound/content/scaffold.py`
- `src/pgfound/content/validate.py`
- `tests/test_phase6_corpus.py`

Multi-session harness references introduced by PROMPT_19:

- `src/pgfound/lab/harness.py`
- `scenarios/concurrency/`
- `docs/concurrency-harness.md`
- `docs/cli.md`
- `src/pgfound/exercise.py`
- `tests/test_harness_runs.py`
- `tests/test_scenario_files_valid.py`

Phase 7a indexing fundamentals references introduced by PROMPT_20:

- `lessons/phase-07-indexing-and-query-plans/`
- `exercises/phase-07-indexing-and-query-plans/`
- `seed-data/packs/ecommerce/phases/phase-07a.sql`
- `seed-data/packs/ecommerce/generators/phase_07a.py`
- `seed-data/packs/scheduling/phases/phase-07a.sql`
- `seed-data/packs/scheduling/generators/phase_07a.py`
- `src/pgfound/lab/explain.py`
- `src/pgfound/content/seed.py`
- `docs/indexing-playbook-part1.md`
- `docs/observability-intro.md`
- `docs/glossary.md`
- `tests/test_phase7a_corpus.py`
