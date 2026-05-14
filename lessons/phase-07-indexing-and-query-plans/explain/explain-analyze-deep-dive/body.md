# EXPLAIN ANALYZE Deep Dive

## Problem Framing

An index recommendation is weak unless the learner can read the plan that proves or disproves it. This lesson goes deeper than naming node types. It focuses on estimated rows, actual rows, loops, buffers, timing, and the places where planner statistics explain surprising choices. The goal is to make a learner slow down before adding another index. Sometimes the problem is not the missing index; it is a bad estimate, stale statistics, correlated columns, or a query shape that hides selectivity.

`EXPLAIN` shows the plan PostgreSQL expects to run. `EXPLAIN ANALYZE` runs the query and shows what happened. `BUFFERS` adds page-read evidence. Together they let the learner compare model and reality. If estimated rows and actual rows are close, the planner had a good model even if the result is still too slow. If estimated rows are off by orders of magnitude, the investigation should turn toward statistics and predicates before more indexes are added.

## Minimal Concept Introduction

A plan is a tree. Each node has a cost estimate, an estimated row count, actual timing, actual rows, and loops. A node that runs once and returns too many rows is different from a node that runs thousands of times because it is inside a nested loop. Buffers reveal whether the query is doing substantial heap or index page work. Timing is useful, but buffers and row counts are more stable across machines.

Extended statistics matter when columns are correlated. Single-column statistics may know the distribution of `tenant_id` and `status` separately but miss that one large tenant owns most open records. `CREATE STATISTICS` can teach PostgreSQL about dependencies, most-common value combinations, or ndistinct relationships. That can change row estimates without adding an index.

## Worked Example

Worked example anchor: tenant-status-row-estimate-mismatch

A SaaS activity query filters by tenant and status:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, tenant_id, status, created_at
FROM saas.activity_events
WHERE tenant_id = '00000000-0000-0000-0000-000000000042'
  AND status = 'open'
ORDER BY created_at DESC
LIMIT 100;
```

The suspicious plan estimates 50 rows but returns 50000 before sorting and limiting. That mismatch can make PostgreSQL choose a nested loop, sort, or index path that looked cheap on paper. Before adding a specialized index, teach the planner about the relationship:

```sql
CREATE STATISTICS activity_events_tenant_status_stats
    (dependencies, mcv)
ON tenant_id, status
FROM saas.activity_events;
ANALYZE saas.activity_events;
```

Run the same plan again. The expected improvement is not always a faster query by itself. The first proof is that estimated rows move closer to actual rows. Once the estimate is honest, an index decision becomes more meaningful. A composite index may still be right, but now it is chosen against a better model.

## Diagnostic Questions

Ask where the largest estimate error appears. Compare estimated rows and actual rows for each node, not only the final result. Ask whether high loops amplify a small per-loop cost. Ask whether buffers are mostly shared hits, reads, or dirtied pages. Ask whether a filter removes many rows after access, which may indicate the index does not match enough predicates. Ask whether stale statistics, correlation, or data skew explain the mismatch.

Also ask whether the query was run with representative parameters. A plan captured for a small tenant may not explain a large tenant. A prepared statement may use a generic plan. A local dev database may not have production skew.

## Common Pitfalls

The common pitfall is reading an index scan as success and a sequential scan as failure. Another is chasing the top cost number while ignoring actual rows and loops. A third is treating timing from a single warm-cache run as proof. A fourth is adding indexes when `ANALYZE` or `CREATE STATISTICS` would address the planner's wrong assumptions. A fifth is comparing before and after plans while changing multiple things at once.

## Explain It Back

A strong explanation says: "The problematic node estimated 50 rows and returned 50000 actual rows, so the planner underpriced the downstream sort and join. Buffers show the query touched far more heap pages than expected. I would run ANALYZE, add `CREATE STATISTICS` for correlated tenant and status columns if needed, then retest the same query before deciding on a composite index." That answer reads the plan as evidence, not decoration.

## References and Further Reading

Use `docs/indexing-playbook-part2.md`, `docs/observability-intro.md`, and PostgreSQL documentation for `EXPLAIN`, planner statistics, and extended statistics.
