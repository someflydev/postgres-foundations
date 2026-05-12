# Operational Rhythm

## Problem Framing

This lesson covers scheduled maintenance and habits that make partition operations boring. The extension track keeps the PostgreSQL core-first doctrine explicit: start with the ordinary PostgreSQL design, name the workload signal that is missing, and only then decide whether pg_partman earns its operational cost. A learner should be able to explain what the tool adds, what remains good enough without it, and what evidence would justify using it in a production cluster. The decision is not a syntax preference. It changes runbooks, failure modes, backup and restore expectations, monitoring, managed-service portability, and the amount of specialized knowledge required from the team that inherits the system. For this topic, the useful habit is to argue from locality, maintenance rhythm, and observed behavior instead of from feature enthusiasm.

## Minimal Concept Introduction

The first concept is scope. pg_partman should be attached to a specific workload, not to a vague feeling that the database might need more power. The second concept is evidence. A responsible design names a baseline query, a representative data volume, an operational symptom, and a measurable outcome. The third concept is reversibility. Extension adoption should include a rollback or migration path, even when that path is slower than the forward change. In this module, the important vocabulary is pg_partman, create_parent, retention, premake, partition_maintenance, partitioning, not_yet_logic. Use those terms to describe behavior that can be observed with SQL, EXPLAIN output, catalog checks, connection behavior, or operational drills. Avoid treating an extension as a shortcut around schema design, indexing, transaction boundaries, or maintenance ownership.

## Worked Example

A useful drill starts from a concrete question, then writes the smallest SQL or configuration check that exposes the evidence. The example below is intentionally compact so an operator can paste it into a runbook, compare it before and after a change, and explain why each clause matters.

```sql
CREATE SCHEMA IF NOT EXISTS partman;
CREATE EXTENSION IF NOT EXISTS pg_partman WITH SCHEMA partman;
SELECT partman.run_maintenance_proc();
```

Read the result as a decision aid, not as a victory lap. If the plan, latency, maintenance behavior, or connection behavior does not change in a way that matters to the workload, the extension has not justified itself. Pair the check with a baseline from the core-only design, a note about write frequency, and a monitoring check that would catch the most likely failure mode after deployment.

## Diagnostic Questions

What user-visible or operator-visible symptom caused this investigation? Which PostgreSQL core feature handles the requirement today, and where does it fail? What metric would improve if pg_partman is the right tool? Which tables, roles, jobs, containers, and dashboards become part of the operational surface? Does the managed service support the required version and settings without special access? How would a restore, failover, rollback, or upgrade be tested? What evidence would make the answer not yet even if the extension can solve a narrow query?

## Common Pitfalls

The first pitfall is enabling an extension because it appears in an architecture diagram. That skips workload evidence and makes later incidents harder to explain. The second pitfall is treating one successful query as a production contract. Operators need representative volume, stale-statistics checks, write-path awareness, and a known owner for maintenance. The third pitfall is ignoring portability. Extension availability varies by image, cloud provider, version, privilege model, and operational maturity. The fourth pitfall is forgetting the core alternative. Citus must be compared with single-node PostgreSQL, tenant-aware schemas, RLS, indexing, and read replicas. ltree must be compared with adjacency lists, recursive CTEs, and closure tables. pg_partman must be compared with core range partitioning and scripted maintenance. PgBouncer must be compared with application pooling and direct connections. A strong recommendation says why the extension is necessary now, or why the team should stay with core PostgreSQL until the signal is stronger.

## Explain It Back

Explain this lesson as a production change request. Name the symptom, the core PostgreSQL behavior that is still useful, the missing capability, the pg_partman feature or configuration you would add, and the verification query you would run after deployment. Then name one case where you would refuse the extension for now. A strong answer is operationally specific: it includes a baseline, a threshold, an owner for maintenance, and a plan for what to do if the result is ambiguous.

## References and Further Reading

Use `docs/doctrine.md` for extension posture, `docs/partitioning-playbook.md` for the partitioning baseline where relevant, `docs/lab.md` for profile startup commands, and the extension-track module docs for this lesson. Pair extension work with the Phase 7 indexing playbooks and the administration monitoring playbook when the change affects production operations.
