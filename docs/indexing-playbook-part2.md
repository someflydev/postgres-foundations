# Indexing Playbook Part 2

Phase 7b adds partial, expression, GIN, GiST, and BRIN indexes. The decision
rule stays the same as Part 1: name the query pattern, prove the data
distribution, measure the plan, and keep the maintenance cost visible.

## Partial Indexes

Use a partial index when a stable, selective predicate defines the hot
workflow. A common example is `ecommerce.orders` where most rows are
`delivered`, but dashboards repeatedly ask for `status = 'pending'`.

Do not use one when application predicates vary, when the rare value is not
actually rare, or when a full composite index serves several important
workloads better.

Verify with `EXPLAIN (ANALYZE, BUFFERS)`. The query predicate must imply the
index `WHERE` clause; otherwise PostgreSQL should ignore the partial index.

## Expression Indexes

Use an expression index when the query consistently filters or sorts by the
same expression, such as `lower(email)` or `date_trunc('day', placed_at)`.

Do not use one to paper over inconsistent application behavior. If one path
uses `lower(email)`, another uses `ILIKE`, and a third normalizes in the app,
standardize the workload first.

Verify that the plan shows the expression index for the same expression text
and semantics. Run `ANALYZE` after creating the index.

## GIN

Use GIN for containment or membership queries over JSONB and arrays. Prefer
`jsonb_path_ops` for compact JSONB containment-only workloads; use default
`jsonb_ops` when broader JSONB operators matter.

Do not use GIN for scalar equality that should be modeled as a normal column,
or for write-heavy data where pending-list churn and bloat exceed query value.

Verify the operator. `payload @> ...` can use a JSONB GIN index; `payload ->>
'key' = ...` usually needs a different design.

## GiST

Use GiST for range overlap, containment, nearest-neighbor-style searches, and
exclusion constraints. Scheduling windows and event windows are the core lab
examples.

Do not use GiST where a simple B-tree predicate answers the workload more
cheaply. GiST is an access-method framework, not a universal upgrade.

Verify the range operator, such as `&&` or `@>`, and compare rows and buffers
before and after the index.

## BRIN

Use BRIN for very large append-heavy tables when the filtered column is
physically correlated with heap order. Time-window filters on event streams are
the canonical example.

Do not use BRIN for randomly updated or physically scrambled data. The index is
small because it summarizes page ranges; summaries are only useful when those
ranges exclude enough pages.

Verify with a realistic time window. Check `Shared Read Blocks`, `Rows Removed
by Index Recheck`, and whether the table's insertion order still tracks the
filtered column.

## Planner Statistics

When estimated rows and actual rows diverge badly, run `ANALYZE` before adding
another index. If two or more columns are correlated, consider extended
statistics:

```sql
CREATE STATISTICS orders_status_placed_stats
ON status, placed_at
FROM ecommerce.orders;
ANALYZE ecommerce.orders;
```

Extended statistics are often the right fix when the planner has the available
index but misjudges how many rows a combined predicate will produce.

## Partitioned Table Indexes

An index declared on a partitioned parent is a partitioned index definition;
the physical work happens on child partitions. There is no single global index
covering all partitions. Design the index around the same workload evidence as
any other table, then verify each new partition receives the expected child
index.

For time-series event logs, a BRIN index on the range key can be useful when
heap order follows time, while B-tree indexes on keys such as `source_id` serve
selective lookups inside the pruned partitions. Keep uniqueness caveats visible:
unique constraints on partitioned parents must include the partition key.
