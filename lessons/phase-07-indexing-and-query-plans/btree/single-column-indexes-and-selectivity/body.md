# Single-column Indexes and Selectivity

## Problem Framing

Phase 7a is where learners start treating query performance as an observable database behavior instead of folklore. This lesson focuses on single-column selectivity. The doctrine stays the same: correctness comes first, and performance advice must be attached to a query pattern. An index is not a decoration on a column. It is an access path that is either useful for a predicate, ordering requirement, and projected column list, or it is extra maintenance work.

The live lab uses the phase 7a seed volume. Ecommerce has more than two hundred thousand orders, more than one million order items, and more than five thousand products. Scheduling has more than fifty thousand appointments across ten professionals. Those sizes are modest enough for a laptop, but large enough that a full table scan is no longer theoretical. Learners should predict, run `EXPLAIN (ANALYZE, BUFFERS)`, read the plan, and explain the tradeoff.

A single-column B-tree is strongest when the column filters to a small fraction of the table. `customer_id = 42` is selective in the generated orders; `status = 'paid'` is not selective because the values are deliberately broad. A low-cardinality index may still appear in a bitmap plan, but that does not prove it is useful for the hot query.

## Minimal Concept Introduction

Start every plan read with the scan node. `Seq Scan` means PostgreSQL is reading table pages and applying the predicate to visible rows. `Index Scan` means PostgreSQL can use an ordered access structure to locate candidate keys and then visit heap rows as needed. `Bitmap Index Scan` plus `Bitmap Heap Scan` means PostgreSQL gathered matching tuple locations first and then visited heap pages in a batched way. `Index Only Scan` means the index can provide the requested columns, although visibility can still require heap checks.

After naming the node, compare estimated rows to actual rows. A poor estimate can explain a surprising plan. Next inspect buffers. Shared hits came from cache; shared reads came from storage. Finally, compare actual time after repeating the test enough to avoid making a decision from one warm-cache accident. In Phase 7a the learner does not need to tune PostgreSQL settings. The learner does need to connect an access path to a concrete workload.

Use `pgfound lab explain` for the local workflow:

```bash
uv run pgfound lab explain --baseline phase7a-before starter.sql
uv run pgfound lab explain --baseline phase7a-after --compare phase7a-before starter.sql
```

Plans are saved under `tmp/plans/`, so a learner can preserve evidence from before and after an index change.

## Worked Example

The lab query for this lesson is:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC;
```

Before the useful index, a representative plan shape is:

```text
Limit  (actual time=38.900..39.100 rows=1 loops=1)
  Buffers: shared hit=13838
  ->  Gather Merge
        ->  Sort
              Sort Key: placed_at DESC
              ->  Seq Scan on orders
                    Filter: (customer_id = 42)
```

The important observation is not the exact millisecond value. The plan reads the table, filters rows, sorts the surviving rows, and only then applies the limit. That is appropriate when no better access path exists, but it is wasteful for a narrow lookup.

Now add the candidate index:

```sql
CREATE INDEX orders_customer_id_phase7a_idx ON ecommerce.orders (customer_id);
ANALYZE;
```

After the index, the representative plan shape is:

```text
Limit  (actual time=0.040..0.080 rows=1 loops=1)
  Buffers: shared hit=8 read=6
  ->  Index Scan using phase7a_candidate_idx on orders
        Index Cond: (customer_id = 42)
```

For scheduling examples the relation name changes, but the reasoning does not: the index gives PostgreSQL a smaller starting region and can provide the required order. For covering examples, watch whether the plan becomes `Index Only Scan`; if it does not, inspect heap fetches and visibility rather than assuming the index failed.

## Diagnostic Questions

- Which predicate defines the smallest useful starting point?
- Does the index key order match equality before range before ordering?
- How many rows did PostgreSQL expect, and how many did it actually see?
- Did the plan reduce heap page visits or only move work from one place to another?
- Which inserts, updates, deletes, and vacuum work now pay for this index?

## Common Pitfalls

Do not confuse distinct value count with usefulness in isolation. Three statuses across two hundred thousand rows means each status can still represent tens of thousands of rows. Another frequent mistake is testing only the happy path. A composite index can serve one query and be useless for another because the leading column sequence is wrong. A covering index can avoid heap fetches for one projection and become needless bloat for a different projection. A low-cardinality single-column index can look reasonable in isolation while slowing the write path that runs all day.

Treat `EXPLAIN ANALYZE` as evidence, not a scoreboard. Explain why the plan changed. If the explanation is just "the time is lower," the reasoning is incomplete. Tie the new plan to index condition, row count, buffer count, and workload cost.

## Explain It Back

Explain this lesson by saying the query pattern first: "For customer_id versus status predicates on the large orders table, I expect this access path because..." Then name the index. A defensible answer includes the predicate, ordering requirement, expected selectivity, and maintenance cost. A weak answer names only a column.

## References and Further Reading

- `docs/indexing-playbook-part1.md` for the Phase 7a cookbook.
- `docs/observability-intro.md` for the `pg_stat_statements` operator tour.
- PostgreSQL documentation on `EXPLAIN`, B-tree indexes, index-only scans, and multicolumn indexes.
