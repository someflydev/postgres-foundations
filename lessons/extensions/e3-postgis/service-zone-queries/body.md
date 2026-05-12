# Service Zone Queries

## Problem Framing

This extension lesson is about logistics service zones, points inside polygons, and distance-bounded fanout. The extension track keeps the core-first doctrine explicit: start with the PostgreSQL feature already available, name the workload signal that is missing, and only then decide whether PostGIS earns its operational cost. A learner should leave this lesson able to say what the extension adds, what remains good enough without it, and what evidence would justify enabling it in a production cluster. The decision is not simply a syntax preference. It touches query plans, statistics, write overhead, backup and restore expectations, replication behavior, upgrade planning, and managed-service portability.

## Minimal Concept Introduction

For Service Zone Queries, the first concept is scope. Spatial data is a domain model with predicates, reference systems, and indexes, not just two numeric columns. The second concept is measurement. Do not ask whether the extension is popular; ask whether the workload has repeated symptoms that core PostgreSQL cannot answer cleanly enough. The third concept is reversibility. A good rollout can be explained with a narrow SQL change, a baseline query, an expected improvement, and a rollback plan. In this repository, extension mastery means using the extension as evidence or capability while keeping the surrounding system understandable to an operator who inherits it later.

## Worked Example

A useful drill starts from a concrete question, then writes the smallest SQL that exposes the evidence. The query below is intentionally compact so the operator can paste it into a runbook, compare it before and after a change, and explain why each column matters.

```sql
SELECT z.zone_name, date_trunc('hour', e.occurred_at) AS hour, count(*) AS events
FROM logistics.service_zones AS z
JOIN logistics.delivery_events AS e
  ON ST_Contains(z.geom, e.geom)
GROUP BY z.zone_name, hour
ORDER BY hour, z.zone_name;
```

Read the output as a decision aid. Sort order tells you the question being asked. A distance ranking asks whether nearby points satisfy a real spatial rule. A semantic ranking asks whether meaning similarity is central to the product behavior. Neither ranking is the final answer by itself. It should lead to an EXPLAIN plan, a threshold discussion, an index review, a product decision, or a not-yet recommendation.

## Diagnostic Questions

What user-visible symptom caused this investigation? Which PostgreSQL core feature handles the requirement today, and where does it fail? What metric or result set would change if PostGIS is the right tool? How often is the underlying data written, and who pays the write or collection overhead? Does the managed service support the required version and settings without superuser-only work? What evidence would prove that the change improved the workload instead of only moving cost elsewhere?

## Common Pitfalls

The first pitfall is enabling an extension because it appears in a recipe. That skips the workload signal and makes later incidents harder to explain. The second pitfall is treating one successful query as a contract. Operators need baselines, representative input, and enough volume to see planner behavior. The third pitfall is ignoring portability. Some extensions are broadly available; others vary by provider or need local operations knowledge. The fourth pitfall is forgetting the core alternative. If a btree lookup, range query, core full-text search, trigram search, generated column, or better EXPLAIN workflow solves the problem, the right answer may be not yet.

## Explain It Back

Explain this lesson as a production change request. Name the symptom, the core PostgreSQL behavior that is still useful, the missing capability, the extension setting or SQL you would add, and the verification query you would run after deploy. Then name one case where you would refuse the extension for now. A strong answer is operationally specific: it includes a baseline, a threshold, an owner for maintenance, and a plan for what to do if the result is ambiguous.

## References and Further Reading

Use `docs/doctrine.md` for extension posture, `docs/search-playbook.md` for search boundaries, and the extension-track module docs for this lesson. Pair extension work with the Phase 7 indexing playbooks and the administration monitoring playbook when the change affects production operations.
