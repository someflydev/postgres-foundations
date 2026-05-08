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
