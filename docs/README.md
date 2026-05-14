# Documentation Index

This index groups the public documentation by reader. It is also the canonical
link map used by `pgfound docs check`.

## Start Here

| Need | Read |
| --- | --- |
| Project doctrine | [Doctrine](doctrine.md) |
| System shape | [Architecture](architecture.md) |
| Repository layout | [Repo Layout](repo-layout.md) |
| CLI surface | [CLI](cli.md) |
| Local PostgreSQL lab | [Lab](lab.md) |
| Glossary | [Glossary](glossary.md) |

## Self-Learner

| Goal | Read |
| --- | --- |
| Work through lessons and exercises | [Learner Workflow](learner-workflow.md) |
| Understand reusable domains | [Domain Conventions](domain-conventions.md) |
| Practice expressive SQL | [Expressive SQL Style](expressive-sql-style.md) |
| Use concurrency scenarios | [Concurrency Harness](concurrency-harness.md) and [Concurrency Playbook](concurrency-playbook.md) |
| Read execution plans | [Observability Intro](observability-intro.md) |
| Track remediation | [Progress and Remediation](progress-and-remediation.md) |

## Coach Or Reviewer

| Goal | Read |
| --- | --- |
| Review exercises and capstones | [Review Engine](review-engine.md) |
| Understand rubric signals | [Rubric Signals](rubric-signals.md) |
| Run interview practice | [Interview Simulator](interview-simulator.md) |
| Use LLM review prompts | [LLM Integration](llm-integration.md), [LLM Provider Neutrality](llm-provider-neutrality.md), and [LLM Usage](llm-usage.md) |
| Review lessons | [Lesson Review Checklist](reviewer-checklists/lesson-review.md) |
| Review exercises | [Exercise Review Checklist](reviewer-checklists/exercise-review.md) |
| Review capstones | [Capstone Review Checklist](reviewer-checklists/capstone-review.md) |
| Review decision rules | [Rule Review Checklist](reviewer-checklists/rule-review.md) |
| Review scenarios | [Scenario Review Checklist](reviewer-checklists/scenario-review.md) |

## Architect

| Goal | Read |
| --- | --- |
| Run planning reports | [Decision Engine Usage](decision-engine-usage.md) |
| Understand scenario fixtures | [Decision Engine Scenarios](decision-engine-scenarios.md) |
| Know current boundaries | [Decision Engine Known Edges](decision-engine-known-edges.md) |
| Keep extension catalogs aligned | [Extension Catalog Sync](extension-catalog-sync.md) |
| Review posture signals | [Capstone Posture Signals](capstone-posture-signals.md) |
| Read decision history | [ADR Index](adr/README.md) |

## Contributor

| Goal | Read |
| --- | --- |
| Author content | [Authoring](authoring.md), [Authoring Lessons](authoring-lessons.md), and [Authoring Exercises](authoring-exercises.md) |
| Understand CI expectations | [CI Requirements](ci-requirements.md) |
| Prepare a release | [Release Readiness](release-readiness.md) and [Known Gaps](known-gaps.md) |
| Use postmortems | [Postmortem Template](postmortem-template.md) |
| Extend admin modules | [Admin Track](admin-track/README.md) |
| Extend extension modules | [Extension Track](extension-track/README.md) |

## PostgreSQL Playbooks And Cookbooks

- [Constraints Cookbook](constraints-cookbook.md)
- [Indexing Playbook Part 1](indexing-playbook-part1.md)
- [Indexing Playbook Part 2](indexing-playbook-part2.md)
- [Search Playbook](search-playbook.md)
- [Partitioning Playbook](partitioning-playbook.md)
- [RLS Playbook](rls-playbook.md)
- [Logical Replication Playbook](logical-replication-playbook.md)

## Admin Track

- [A1 Roles Playbook](admin-track/a1-roles-playbook.md)
- [A2 Schemas Playbook](admin-track/a2-schemas-playbook.md)
- [A3 Auth And Pooling Playbook](admin-track/a3-auth-and-pooling-playbook.md)
- [A4 Backup And Upgrades Playbook](admin-track/a4-backup-and-upgrades-playbook.md)
- [A5 Monitoring Playbook](admin-track/a5-monitoring-playbook.md)
- [A6 Replication HA Playbook](admin-track/a6-replication-ha-playbook.md)

## Extension Track

- [E1 pg_stat_statements](extension-track/e1-pg-stat-statements.md)
- [E2 pg_trgm](extension-track/e2-pg-trgm.md)
- [E3 PostGIS](extension-track/e3-postgis.md)
- [E4 pgvector](extension-track/e4-pgvector.md)
- [E5 TimescaleDB](extension-track/e5-timescaledb.md)
- [E6 postgres_fdw](extension-track/e6-postgres-fdw.md)
- [E7 Citus](extension-track/e7-citus.md)
- [ltree](extension-track/ltree.md)
- [pg_partman](extension-track/pg_partman.md)
- [PgBouncer](extension-track/pgbouncer.md)

## Anti-Patterns

- [Arrays Over Child Tables](anti-patterns/arrays_over_child_tables.md)
- [FDW Without Pushdown Verification](anti-patterns/fdw_without_pushdown_verification.md)
- [Geo Logic Without PostGIS](anti-patterns/geo_logic_without_postgis.md)
- [JSONB Everything](anti-patterns/jsonb_everything.md)
- [Naive Wall Clock Timestamp](anti-patterns/naive_wall_clock_timestamp.md)
- [No Pooling For High Connections](anti-patterns/no_pooling_high_connections.md)
- [No Restore Drills](anti-patterns/no_restore_drills.md)
- [Partition Too Early](anti-patterns/partition_too_early.md)
- [Redundant Indexes](anti-patterns/redundant_indexes.md)
- [Replica As Performance Bandage](anti-patterns/replica_as_performance_bandage.md)
- [Shard Without Distribution Key](anti-patterns/shard_without_distribution_key.md)
- [Timescale Too Early](anti-patterns/timescale_too_early.md)
- [Unused Indexes](anti-patterns/unused_indexes.md)
- [Vacuum Starvation By Long Transaction](anti-patterns/vacuum_starvation_by_long_txn.md)
- [Vector Before Lexical](anti-patterns/vector_before_lexical.md)

## ADRs

- [ADR 0001: Python, uv, Ruff, and pytest](adr/0001-python-uv-ruff-pytest-toolchain.md)
- [ADR 0002: JSON-first content model](adr/0002-json-first-content-model.md)
- [ADR 0003: Docker for the lab](adr/0003-docker-for-the-lab.md)
- [ADR 0004: Core-first extension doctrine](adr/0004-core-first-extension-doctrine.md)
- [ADR 0005: Explainable decision engine](adr/0005-decision-engine-is-explainable.md)
- [ADR Template](adr/template.md)
