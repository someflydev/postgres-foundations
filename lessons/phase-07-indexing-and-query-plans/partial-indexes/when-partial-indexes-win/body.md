# When Partial Indexes Win

## Problem Framing

Partial indexes are for workloads where the important rows are a small, stable slice of a larger table. The point is not to show that PostgreSQL can attach a WHERE clause to an index. The point is to prove that a repeated query only needs a subset of the table, and that maintaining index entries for the rest of the rows would be waste. This lesson keeps the pending orders dashboard as the canonical Phase 7b example because it has the right shape: a hot operational query, a skewed status distribution, and a predicate the learner can defend.

A useful partial index starts with the query text, not with the index definition. If the query is written as `status = 'pending'`, the index predicate must match that implication. If the production query says `status IN ('pending', 'refunded')`, a narrower index may not be usable. If the status values stop being rare, the index may stop winning. Partial indexes are therefore operational promises. They promise that the hot slice remains hot, small, and named consistently enough for the planner to use.

## Minimal Concept Introduction

A normal B-tree on `status` contains delivered, canceled, refunded, and pending rows. If delivered rows dominate the table, that index spends most of its storage and write maintenance on rows the dashboard will never read. A partial index can store only the rows that match the predicate and order them by the access pattern the query needs. Smaller size can mean fewer pages, better cache behavior, and less write amplification, but only for queries whose predicates imply the partial index predicate.

This is where planner honesty matters. PostgreSQL will not use a partial index because a human can see that two expressions feel related. It needs a provable implication from the query condition to the index condition. Parameters, broad inequalities, function-wrapped columns, and application-side condition builders can all hide that implication.

## Worked Example

Worked example anchor: pending-orders-partial-index

Suppose the operations dashboard asks for pending orders every minute:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE status = 'pending'
ORDER BY placed_at DESC
LIMIT 50;
```

Start by measuring the baseline. A sequential scan may be reasonable on a tiny table, but not on a multi-million-row order table where only a small fraction are pending. A full index on `(status, placed_at)` may help reads, but it still stores every status value. The partial index records the workload more precisely:

```sql
CREATE INDEX orders_pending_recent_idx
ON ecommerce.orders (placed_at DESC)
WHERE status = 'pending';
ANALYZE ecommerce.orders;
```

Run the same `EXPLAIN (ANALYZE, BUFFERS)` again. A strong result is not merely the appearance of `orders_pending_recent_idx`. The proof is fewer heap pages read, fewer rows removed by filter, a plan that can satisfy the ordering and stop early for the `LIMIT`, and estimates that are close enough to actual rows to trust. If estimates are badly wrong, run `ANALYZE` and inspect statistics before adding more indexes.

## Diagnostic Questions

Ask what exact query benefits, how many rows satisfy the predicate, whether the predicate is stable over time, and whether the application always emits the same condition. Ask what writes now maintain the index. An order that enters and leaves pending status may still create index churn. A status value that was rare during the first month may become common after a product change. A prepared statement that hides constants may prevent predicate implication in places where a literal worked during a demo.

Also ask what the index does not solve. It does not make `status <> 'delivered'` equivalent to pending. It does not accelerate a report that mixes pending and refunded rows unless that broader predicate has its own justified index. It does not replace a better state model if the real issue is ambiguous order lifecycle semantics.

## Common Pitfalls

The first pitfall is creating a partial index from a dashboard screenshot without verifying production SQL. The second is leaving a broader redundant index in place, so writes pay for both the full index and the partial index. The third is celebrating lower estimated cost without checking buffers and actual rows. The fourth is forgetting removal criteria. A partial index should have a drop condition, such as low scan count, changed status distribution, or replacement by a different dashboard query.

## Explain It Back

A good explanation names the hot slice, the predicate, the ordering, and the cost. For example: "The dashboard reads rare pending orders by recent time. The partial index contains only rows where `status = 'pending'` and is ordered by `placed_at DESC`, so the planner can avoid delivered rows and stop early. It is cheaper to maintain than a full status index, but only while the query predicate remains stable and pending rows stay rare." That is the level of operational reasoning this lesson expects.

## References and Further Reading

Use `docs/indexing-playbook-part2.md` for the Phase 7b checklist and `docs/indexing-playbook-part1.md` when you need to revisit B-tree access paths, ordering, and selectivity.
