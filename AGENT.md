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
- CLI smoke: `uv run pgfound --help`
- Decision stub run: `uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json`
- Content validate: `uv run pgfound content validate`
- Content examples validate: `uv run pgfound content validate --include-examples`
- Content lint: `uv run pgfound content lint`
- Seed doctor: `uv run pgfound content seed-doctor`
- Seed dry-run: `uv run pgfound content seed ecommerce --phase 1 --dry-run`
- Seed lab data: `uv run pgfound content seed ecommerce --phase 7b --reset --generate`
- Seed scheduling lab data: `uv run pgfound content seed scheduling --phase 7a --reset --generate`
- Seed event indexing lab data: `uv run pgfound content seed event_heavy_ops --phase 7b --reset`
- Seed document FTS lab data: `uv run pgfound content seed document_search --phase 8 --reset --generate`
- Seed logistics geo lab data: `PGFOUND_DB_URL=postgresql://pgfound:pgfound@localhost:5436/pgfound uv run pgfound content seed logistics_geo --phase 1 --reset`
- Seed ecommerce FTS lab data: `uv run pgfound content seed ecommerce --phase 8 --reset --generate`
- Seed event partitioning lab data: `uv run pgfound content seed event_heavy_ops --phase 9 --reset --generate`
- Seed ecommerce partitioning lab data: `uv run pgfound content seed ecommerce --phase 9 --reset --generate`
- Seed SaaS RLS lab data: `uv run pgfound content seed saas_multi_tenant --phase 10 --reset`
- Seed modernization FDW lab data: `uv run pgfound content seed modernization_bridge --phase 10 --reset`
- Apply admin role matrix: `psql "postgresql://pgfound:pgfound@localhost:55433/pgfound" -v ON_ERROR_STOP=1 -f seed-data/packs/admin/roles-matrix.sql`
- Run admin access review queries: `psql "postgresql://pgfound:pgfound@localhost:55433/pgfound" -v ON_ERROR_STOP=1 -f seed-data/packs/admin/access-review-queries.sql`
- HBA overlay lab up: `docker compose -f docker/docker-compose.yml --profile hba_overlay up -d pg-hba-overlay`
- PgBouncer pooling lab up: `docker compose -f docker/docker-compose.yml --profile pooling up -d`
- Restore drill: `scripts/restore-drill.sh`
- Replication lab up: `docker compose -f docker/docker-compose.yml --profile replication up -d`
- PostGIS lab up: `docker compose -f docker/docker-compose.yml --profile postgis up -d postgis`
- pgvector lab up: `docker compose -f docker/docker-compose.yml --profile pgvector up -d pgvector`
- TimescaleDB lab up: `docker compose -f docker/docker-compose.yml --profile timescale up -d timescale`
- Citus lab up: `docker compose -f docker/docker-compose.yml --profile citus up -d citus-coordinator citus-worker-1 citus-worker-2`
- pg_partman lab up: `docker compose -f docker/docker-compose.yml --profile pgpartman up -d pgpartman`
- Ops top statements: `uv run pgfound ops query top-by-total-time`
- Ops blocking chain: `uv run pgfound ops query blocking-chain`
- Ops replica lag: `uv run pgfound ops query replica-lag`
- Exercise dry-run: `uv run pgfound exercise run first-select-write-query --dry-run`
- Exercise check: `uv run pgfound exercise run first-select-write-query --check`
- Exercise timing check: `uv run pgfound exercise run what-lateral-unlocks-level-c-1 --check --answer exercises/phase-05-expressive-querying/what-lateral-unlocks/level-c/what-lateral-unlocks-level-c-1/solution.sql --no-prompt --timing`
- Concurrency scenario list: `uv run pgfound lab concurrency list`
- Concurrency scenario run: `uv run pgfound lab concurrency run scenarios/concurrency/inventory-lost-update.yaml`
- Capstone start: `uv run pgfound capstone start 01-multi-tenant-saas-crm`
- Exercise review: `uv run pgfound exercise review first-select-write-query --answer tmp/answers/first-select-write-query.sql --auto`
- Capstone evaluation: `uv run pgfound capstone evaluate 01-multi-tenant-saas-crm --path tmp/capstone-work/01-multi-tenant-saas-crm`
- Capstone full evaluation: `uv run pgfound capstone evaluate 01-multi-tenant-saas-crm --path capstones/01-multi-tenant-saas-crm/reference --full`
- Review engine: `uv run pgfound review run --exercise-id first-select-write-query --answer tmp/answers/first-select-write-query.sql`
- LLM prompt list: `uv run pgfound llm list`
- LLM prompt render: `uv run pgfound llm render critique/query-critique --context tests/fixtures/critique-context.json --out tmp/preview.md`
- Interview start: `uv run pgfound interview start --scenario senior-backend-saas-rls`
- Interview review: `uv run pgfound interview review tmp/interviews/<scenario-id>/<timestamp>.md`
- Interview dispatch bundle: `uv run pgfound interview dispatch tmp/interviews/<scenario-id>/<timestamp>.md`
- Capstone scheduling concurrency check: `uv run pgfound lab concurrency run scenarios/concurrency/scheduling-double-booking.yaml`
- Explain plan: `uv run pgfound lab explain <sql-file-or-inline>`
- Progress summary: `uv run pgfound progress show`
- Lab up: `make lab-up`
- Lab down: `make lab-down`
- Lab reset: `make lab-nuke`
- Lab psql: `make lab-psql`
- Lab reset domain: `uv run pgfound lab reset-domain ecommerce`
- Lab snapshot: `uv run pgfound lab snapshot <name>`
- Lab restore: `uv run pgfound lab restore <name>`

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
