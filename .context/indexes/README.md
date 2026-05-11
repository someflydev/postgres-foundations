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

Interview simulator references introduced by PROMPT_28:

- `src/pgfound/interview/`
- `scenarios/interviews/*.yaml`
- `content-schemas/interview-scenario.schema.json`
- `rubrics/interview/*.rubric.json`
- `llm-prompts/interview/stages/*.md`
- `docs/interview-simulator.md`
- `tests/test_interview_scenarios.py`
- `tests/test_interview_session_stubbed.py`

Training-side LLM prompt references introduced by PROMPT_29:

- `llm-prompts/README.md`
- `llm-prompts/template-format.md`
- `llm-prompts/coaching/*.md`
- `llm-prompts/critique/*.md`
- `llm-prompts/remediation/*.md`
- `llm-prompts/shared/`
- `src/pgfound/llm/`
- `docs/llm-usage.md`
- `docs/llm-integration.md`
- `tests/test_llm_templates.py`
- `tests/test_llm_render_cli.py`
- `tests/test_template_completeness.py`

Administration track references introduced by PROMPT_31:

- `curriculum/admin/map.json`
- `lessons/admin/a1-roles-and-privileges/`
- `lessons/admin/a2-schemas-and-databases/`
- `exercises/admin/a1-roles-and-privileges/`
- `exercises/admin/a2-schemas-and-databases/`
- `seed-data/packs/admin/roles-matrix.sql`
- `seed-data/packs/admin/access-review-queries.sql`
- `docs/admin-track/README.md`
- `docs/admin-track/a1-roles-playbook.md`
- `docs/admin-track/a2-schemas-playbook.md`
- `content-schemas/admin-map.schema.json`
- `tests/test_admin_map.py`
- `tests/test_admin_a1_a2_corpus.py`

Administration track references introduced by PROMPT_32:

- `lessons/admin/a3-auth-and-pooling/`
- `lessons/admin/a4-maintenance-and-lifecycle/`
- `exercises/admin/a3-auth-and-pooling/`
- `exercises/admin/a4-maintenance-and-lifecycle/`
- `docs/admin-track/a3-auth-and-pooling-playbook.md`
- `docs/admin-track/a4-backup-and-upgrades-playbook.md`
- `docker/hba_overlay/pg_hba.conf`
- `docker/pgbouncer/pgbouncer.ini`
- `scripts/restore-drill.sh`
- `tests/test_admin_a3_a4_corpus.py`
- `tests/test_pgbouncer_compose.py`

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

Phase 8 PostgreSQL full-text search references introduced by PROMPT_22:

- `lessons/phase-08-postgresql-full-text-search/`
- `exercises/phase-08-postgresql-full-text-search/`
- `seed-data/packs/document_search/phases/phase-08.sql`
- `seed-data/packs/document_search/generators/documents_csv.py`
- `seed-data/packs/ecommerce/phases/phase-08.sql`
- `docker/initdb/00-extensions.sql`
- `docs/search-playbook.md`
- `docs/lab.md`
- `tests/test_phase8_corpus.py`
- `tests/test_document_corpus.py`

Phase 9 partitioning references introduced by PROMPT_23:

- `lessons/phase-09-partitioning-and-large-table-operations/`
- `exercises/phase-09-partitioning-and-large-table-operations/`
- `seed-data/packs/event_heavy_ops/phases/phase-09.sql`
- `seed-data/packs/event_heavy_ops/generators/phase_09.py`
- `seed-data/packs/ecommerce/phases/phase-09.sql`
- `docs/partitioning-playbook.md`
- `docs/anti-patterns/partition_too_early.md`
- `docs/indexing-playbook-part2.md`
- `tests/test_phase9_corpus.py`
- `tests/test_partitioning_seed.py`

Phase 10 security and federation references introduced by PROMPT_24:

- `lessons/phase-10-roles-rls-replication-and-fdw/`
- `exercises/phase-10-roles-rls-replication-and-fdw/`
- `seed-data/packs/saas_multi_tenant/phases/phase-10.sql`
- `seed-data/packs/modernization_bridge/phases/phase-10.sql`
- `docker/initdb-replica/00-init.sql`
- `docker/initdb/20-replication-role.sql`
- `docs/rls-playbook.md`
- `docs/logical-replication-playbook.md`
- `docs/lab.md`
- `tests/test_phase10_corpus.py`
- `tests/test_rls_policy_sql.py`

Capstone references introduced by PROMPT_25:

- `capstones/01-multi-tenant-saas-crm/`
- `capstones/02-scheduling-availability/`
- `scenarios/concurrency/scheduling-double-booking.yaml`
- `content-schemas/rubric.schema.json`
- `src/pgfound/cli.py`
- `src/pgfound/content/validate.py`
- `docs/authoring-exercises.md`
- `docs/cli.md`
- `tests/test_capstone_corpus.py`
- `tests/test_capstone_start_cli.py`

Capstone references introduced by PROMPT_26:

- `capstones/03-event-heavy-ops/`
- `capstones/04-modernization-bridge/`
- `capstones/README.md`
- `rubrics/default/extension-posture.rubric.json`
- `rubrics/default/operational-reasoning.rubric.json`
- `scenarios/concurrency/legacy-fdw-stale-matview.yaml`
- `exercises/phase-10-roles-rls-replication-and-fdw/modernization-bridge-pattern/level-d/modernization-bridge-pattern-level-d-3/`
- `tests/test_capstones_all.py`
- `tests/test_extension_posture_rubric.py`

Review engine references introduced by PROMPT_27:

- `src/pgfound/review/engine.py`
- `src/pgfound/review/grading.py`
- `src/pgfound/review/models.py`
- `src/pgfound/review/runners/`
- `src/pgfound/review/output/`
- `docs/review-engine.md`
- `docs/rubric-signals.md`
- `tests/test_review_engine_exercise.py`
- `tests/test_review_engine_capstone.py`
- `tests/test_plan_diff.py`
