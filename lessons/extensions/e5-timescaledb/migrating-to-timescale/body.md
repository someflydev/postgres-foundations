# Migrating To Timescale

## Problem Framing

This lesson covers moving an existing partitioned events workload into a hypertable and planning a practical revert path. The extension track keeps the PostgreSQL core-first doctrine explicit: start with the ordinary PostgreSQL design, name the workload signal that is missing, and only then decide whether TimescaleDB earns its operational cost. A learner should be able to explain what the extension adds, what remains good enough without it, and what evidence would justify using it in a production cluster. The decision is not a syntax preference. It changes runbooks, failure modes, backup and restore expectations, monitoring, managed-service portability, and the amount of specialized knowledge required from the team that inherits the system.

## Minimal Concept Introduction

The first concept is scope. TimescaleDB should be attached to a specific workload, not to a vague feeling that the database might need more power. The second concept is evidence. A responsible design names a baseline query, a representative data volume, an operational symptom, and a measurable outcome. The third concept is reversibility. Extension adoption should include a rollback or migration path, even when that path is slower than the forward change. In this module, the important vocabulary is hypertables, chunks, continuous aggregates, compression, retention policies, background workers, licensing boundaries, and upgrade posture. Use those terms to describe behavior that can be observed with SQL, EXPLAIN output, catalog checks, or operational drills.

## Worked Example

A useful drill starts from a concrete question, then writes the smallest SQL that exposes the evidence. The query below is intentionally compact so an operator can paste it into a runbook, compare it before and after a change, and explain why each clause matters.

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;
SELECT create_hypertable('events.event_log_timescale', by_range('occurred_at'), if_not_exists => TRUE);
SELECT time_bucket('1 hour', occurred_at) AS hour, count(*)
FROM events.event_log_timescale
GROUP BY hour
ORDER BY hour DESC
LIMIT 24;
```

Read the result as a decision aid, not as a victory lap. If the plan, latency, or maintenance behavior does not change in a way that matters to the workload, the extension has not justified itself. Pair the query with a baseline from the core-only design, a note about write frequency, and a monitoring check that would catch the most likely failure mode after deployment.

## Diagnostic Questions

What user-visible or operator-visible symptom caused this investigation? Which PostgreSQL core feature handles the requirement today, and where does it fail? What metric would improve if TimescaleDB is the right tool? Which tables, roles, jobs, and dashboards become part of the operational surface? Does the managed service support the required version and settings without special access? How would a restore, failover, or upgrade be tested? What evidence would make the answer not yet even if the extension can solve a narrow query?

## Common Pitfalls

The first pitfall is enabling an extension because it appears in an architecture diagram. That skips workload evidence and makes later incidents harder to explain. The second pitfall is treating one successful query as a production contract. Operators need representative volume, stale-statistics checks, write-path awareness, and a known owner for maintenance. The third pitfall is ignoring portability. Extension availability varies by image, cloud provider, version, and privilege model. The fourth pitfall is forgetting the core alternative. Phase 9 partitioning remains the default comparison point. Core range partitions, BRIN indexes, retention by detach or drop, and ordinary materialized views are often enough until time-series analytics becomes central. A strong recommendation says why the extension is necessary now, or why the team should stay with core PostgreSQL until the signal is stronger.

## Explain It Back

Explain this lesson as a production change request. Name the symptom, the core PostgreSQL behavior that is still useful, the missing capability, the TimescaleDB feature or configuration you would add, and the verification query you would run after deployment. Then name one case where you would refuse the extension for now. A strong answer is operationally specific: it includes a baseline, a threshold, an owner for maintenance, and a plan for what to do if the result is ambiguous.

## References and Further Reading

Use `docs/doctrine.md` for extension posture, `docs/partitioning-playbook.md` for the partitioning baseline, `docs/logical-replication-playbook.md` for consolidation paths, and the extension-track module docs for this lesson. Pair extension work with the Phase 7 indexing playbooks and the administration monitoring playbook when the change affects production operations.
