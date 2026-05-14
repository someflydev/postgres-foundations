# postgres-foundations

A serious PostgreSQL learning and planning platform: structured curriculum, hands-on Docker lab, admin + extension mastery, and an explainable PostgreSQL architecture decision engine.

`postgres-foundations` is a public training and planning repo for people who need to learn PostgreSQL as a system, not as a loose set of syntax tricks. It combines curriculum, executable labs, review workflows, operational drills, extension posture, and a rules-backed decision engine that turns workload signals into explainable architecture guidance.

## What's Inside

- Curriculum: phase 0-10 learning path from database reality and SQL basics through indexing, search, partitioning, RLS, replication, and FDW.
- Lab: Docker Compose PostgreSQL environments, seed packs, reset/snapshot helpers, explain-plan tooling, and multi-session concurrency harnesses.
- Admin track: role design, schema governance, auth and pooling, backup and upgrade drills, monitoring, replication, and HA practice.
- Extension track: `pg_stat_statements`, `pg_trgm`, PostGIS, pgvector, TimescaleDB, `postgres_fdw`, Citus, `ltree`, `pg_partman`, and PgBouncer.
- Capstones: multi-file system design exercises with starter artifacts, reference implementations, rubrics, review reports, and posture signals.
- Interview simulator: scenario-based technical interviews with transcript capture, review, and dispatch bundles.
- Decision engine: JSON catalogs, declarative rules, scoring, reports, scenario fixtures, and follow-up questions.
- Scenario packs: reusable domain data, concurrency scenarios, capstone scenarios, interview scenarios, and industry architecture cases.
- Prompt packs: training-side coaching/review prompts and four-layer decision-engine prompt packs for catalog, evaluator, scenario, and critique work.

## Who This Is For

This repo is for self-learners who want a structured route from zero to practical PostgreSQL competence; coaches and reviewers who need concrete artifacts to evaluate; architects who want a core-first planning vocabulary; and teams making PostgreSQL strategy decisions under real operational constraints and shared review pressure.

It is not a generic LMS, a blog, or a vendor-neutral database survey. It is PostgreSQL-first and PostgreSQL-core-first. Extensions are treated as operational commitments that require evidence, not as collectibles.

## Quickstart

```bash
git clone https://github.com/someflydev/postgres-foundations.git
cd postgres-foundations
uv sync
docker compose -f docker/docker-compose.yml up -d pg
uv run pgfound doctor
uv run pgfound content seed ecommerce --phase 1
uv run pgfound exercise run first-select-write-query --dry-run
uv run pgfound exercise run first-select-write-query --check
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json --format markdown --show-scores
uv run pgfound progress show
```

## Directory Map

- `.context/`: short agent-facing state, prompt log, and execution runbooks.
- `.prompts/`: monotonic build prompts that define the repo construction sequence.
- `capstones/`: capstone briefs, starters, references, rubrics, and acceptance criteria.
- `content-schemas/`: JSON Schemas, examples, and templates for authored learning content.
- `curriculum/`: phase maps, admin and extension maps, domain notes, and capability layers.
- `decision-engine/`: planning catalogs, rules, schemas, prompt packs, fixtures, and reports.
- `docker/`: Docker Compose lab services, init scripts, extension profiles, and PgBouncer config.
- `docs/`: architecture, doctrine, workflows, playbooks, ADRs, and reviewer guidance.
- `exercises/`: active learner exercises for curriculum phases, admin modules, and extensions.
- `lessons/`: active lessons and worked examples aligned to exercise sets.
- `llm-prompts/`: provider-neutral prompt templates for coaching, critique, remediation, interviews, and capstone review.
- `rubrics/`: default, interview, and composed assessment rubrics.
- `scenarios/`: concurrency, capstone, interview, and industry scenario packs.
- `scripts/`: validation, golden refresh, restore drill, monitoring, and lint helper scripts.
- `seed-data/`: reusable PostgreSQL data packs and deterministic generators.
- `src/pgfound/`: Python package and Click CLI implementation.
- `tests/`: unit and integration tests for content, CLI, lab tooling, review, progress, and decision behavior.

## Doctrine

- Core first: prefer PostgreSQL built-ins until workload evidence justifies more.
- "Not yet" is a valid recommendation when capability would add premature burden.
- Explainability matters: recommendations must name signals, tradeoffs, and operational consequences.

Read the full doctrine in [docs/doctrine.md](docs/doctrine.md).

## Status and Roadmap

The repo currently contains the full platform surface: curriculum and exercises, lab tooling, admin and extension tracks, capstones, review workflows, interview simulation, progress and remediation flows, decision-engine catalogs/rules/scoring, scenario fixtures, public documentation, CI, pre-commit configuration, and release-readiness checks. Remaining release caveats are tracked in [docs/known-gaps.md](docs/known-gaps.md).

Architecture decisions are recorded under [docs/adr/](docs/adr/). The ADRs explain why the repo uses Python with `uv`, JSON-first content, Docker for the lab, a core-first extension doctrine, and an explainable decision engine.

## How To Use It

If you want to learn PostgreSQL from zero, start with [curriculum/README.md](curriculum/README.md), then follow [docs/learner-workflow.md](docs/learner-workflow.md). Use the Docker lab, seed packs, exercises, review command, and progress dashboard as the main loop.

If you want to level up operationally, start with [docs/admin-track/README.md](docs/admin-track/README.md) and [docs/extension-track/README.md](docs/extension-track/README.md). Those tracks assume core competence and move into roles, pooling, restore drills, monitoring, replication, extension posture, and operational tradeoffs.

If you want to plan a PostgreSQL architecture, start with [docs/decision-engine-usage.md](docs/decision-engine-usage.md), inspect the fixtures under [decision-engine/fixtures/intakes/](decision-engine/fixtures/intakes/), and run `uv run pgfound decision run <intake>`. Use [docs/decision-engine-scenarios.md](docs/decision-engine-scenarios.md) for industry examples and [docs/decision-engine-known-edges.md](docs/decision-engine-known-edges.md) for boundaries.

## License And Attribution

This project is released under the [MIT License](LICENSE) unless otherwise specified. Authorship is tracked in [AUTHORS.md](AUTHORS.md).
