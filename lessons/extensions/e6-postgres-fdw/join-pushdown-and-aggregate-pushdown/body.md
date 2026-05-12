# Join Pushdown And Aggregate Pushdown

## Problem Framing

This lesson covers PostgreSQL 14 and newer join and aggregate pushdown with EXPLAIN VERBOSE verification. The extension track keeps the PostgreSQL core-first doctrine explicit: start with the ordinary PostgreSQL design, name the workload signal that is missing, and only then decide whether postgres_fdw earns its operational cost. A learner should be able to explain what the extension adds, what remains good enough without it, and what evidence would justify using it in a production cluster. The decision is not a syntax preference. It changes runbooks, failure modes, backup and restore expectations, monitoring, managed-service portability, and the amount of specialized knowledge required from the team that inherits the system.

## Minimal Concept Introduction

The first concept is scope. postgres_fdw should be attached to a specific workload, not to a vague feeling that the database might need more power. The second concept is evidence. A responsible design names a baseline query, a representative data volume, an operational symptom, and a measurable outcome. The third concept is reversibility. Extension adoption should include a rollback or migration path, even when that path is slower than the forward change. In this module, the important vocabulary is foreign servers, user mappings, remote SQL, predicate pushdown, join pushdown, aggregate pushdown, async append, statistics, SSL, and timeout posture. Use those terms to describe behavior that can be observed with SQL, EXPLAIN output, catalog checks, or operational drills.

## Worked Example

A useful drill starts from a concrete question, then writes the smallest SQL that exposes the evidence. The query below is intentionally compact so an operator can paste it into a runbook, compare it before and after a change, and explain why each clause matters.

```sql
EXPLAIN (VERBOSE, COSTS OFF)
SELECT external_order_ref, external_customer_ref, order_total
FROM legacy_fdw.legacy_orders
WHERE currency = 'USD'
  AND order_total >= 100;
```

Read the result as a decision aid, not as a victory lap. If the plan, latency, or maintenance behavior does not change in a way that matters to the workload, the extension has not justified itself. Pair the query with a baseline from the core-only design, a note about write frequency, and a monitoring check that would catch the most likely failure mode after deployment.

## Diagnostic Questions

What user-visible or operator-visible symptom caused this investigation? Which PostgreSQL core feature handles the requirement today, and where does it fail? What metric would improve if postgres_fdw is the right tool? Which tables, roles, jobs, and dashboards become part of the operational surface? Does the managed service support the required version and settings without special access? How would a restore, failover, or upgrade be tested? What evidence would make the answer not yet even if the extension can solve a narrow query?

## Common Pitfalls

The first pitfall is enabling an extension because it appears in an architecture diagram. That skips workload evidence and makes later incidents harder to explain. The second pitfall is treating one successful query as a production contract. Operators need representative volume, stale-statistics checks, write-path awareness, and a known owner for maintenance. The third pitfall is ignoring portability. Extension availability varies by image, cloud provider, version, and privilege model. The fourth pitfall is forgetting the core alternative. Phase 10 introduced federation as a bridge, not as a permanent excuse to hide ownership. A local table, logical replication, or a deliberate service boundary may be clearer than another remote join. A strong recommendation says why the extension is necessary now, or why the team should stay with core PostgreSQL until the signal is stronger.

## Explain It Back

Explain this lesson as a production change request. Name the symptom, the core PostgreSQL behavior that is still useful, the missing capability, the postgres_fdw feature or configuration you would add, and the verification query you would run after deployment. Then name one case where you would refuse the extension for now. A strong answer is operationally specific: it includes a baseline, a threshold, an owner for maintenance, and a plan for what to do if the result is ambiguous.

## References and Further Reading

Use `docs/doctrine.md` for extension posture, `docs/partitioning-playbook.md` for the partitioning baseline, `docs/logical-replication-playbook.md` for consolidation paths, and the extension-track module docs for this lesson. Pair extension work with the Phase 7 indexing playbooks and the administration monitoring playbook when the change affects production operations.
