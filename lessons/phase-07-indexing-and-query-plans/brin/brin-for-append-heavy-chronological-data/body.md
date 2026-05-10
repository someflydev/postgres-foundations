# BRIN for Append Heavy Chronological Data

## Problem Framing

Phase 7b starts from a stricter rule than a catalog tour: every index exists because a concrete query pattern and a real data distribution made it a better tradeoff than the alternatives. BRIN for Append Heavy Chronological Data is taught through that rule. A learner should be able to point at the predicate, join key, sort key, containment operator, or range operator that creates the need. They should also be able to point at the rows that will not benefit, because those rows still pay storage and maintenance cost when an index is too broad.

The working domains are intentionally familiar. Ecommerce orders give us a skewed status distribution where delivered orders dominate and pending, refunded, and canceled rows are operationally hot but rare. Event-heavy operations give us append-heavy rows where occurred_at usually tracks physical insertion order. Scheduling gives us time ranges that can overlap, contain one another, and require exclusion-style correctness. Phase 4b introduced arrays, ranges, and JSONB as modeling tools; this lesson returns to them with the planner in the room.

The central operational question is not "can PostgreSQL create this index?" The question is "which repeated query becomes cheaper, how do we prove it, and what does the system now have to maintain?" A full B-tree on status may be an attractive first guess, but if most rows have the same value it can be a poor access path. A partial index can be excellent when the predicate is stable and exactly matches the hot workflow. A GIN index can be decisive for JSONB containment and array membership, yet expensive to build and maintain. GiST can support range overlap and exclusion logic, but it is not a universal replacement for B-tree. BRIN can summarize large chronological tables in tiny storage, but only when physical correlation makes those summaries selective enough.

## Minimal Concept Introduction

The planner matches query predicates to available access paths using operator classes, statistics, row estimates, and cost settings. In this lesson the required vocabulary includes BRIN, physical correlation, append-heavy. The practical habit is always the same: write the slow or suspicious query, run EXPLAIN or EXPLAIN ANALYZE BUFFERS, read the estimated rows and actual rows, then change one thing. After the change, run the same query again and compare the plan. The goal is not merely to see an index name. The goal is to see fewer pages read, fewer rows filtered after access, a lower cost estimate when statistics support it, or a more appropriate node type for the data shape.

Partial indexes add a WHERE clause to the index definition. PostgreSQL can use the index only when the query predicate implies that WHERE clause. This is why a partial index on status = 'pending' is not automatically used by a query that says status IN ('pending', 'refunded'), even when pending is one of the values. Expression indexes store the result of an expression such as lower(email) or date_trunc('day', created_at). They are powerful when application queries consistently use the same expression, but fragile when the query drifts to a different expression or time zone rule.

GIN indexes invert membership-like structures: JSONB keys and values, array elements, and later full-text lexemes. The default jsonb_ops class supports more operators; jsonb_path_ops is smaller and targeted for containment. GiST indexes are a framework for search trees over shapes, ranges, and many extension types. For ranges, GiST supports operators such as && and @>. BRIN stores summaries for ranges of heap pages. It is often the right first thought for very large append-heavy event tables filtered by time.

## Worked Example

Suppose the operations dashboard asks for pending orders every minute:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE status = 'pending'
ORDER BY placed_at DESC
LIMIT 50;
```

A full index on status may still carry entries for every delivered order. If delivered rows are more than ninety percent of the table, that index is larger than the hot query needs, and it must be updated for rows the dashboard will never read. A partial index can encode the actual workload:

```sql
CREATE INDEX orders_pending_recent_idx
ON ecommerce.orders (placed_at DESC)
WHERE status = 'pending';
ANALYZE ecommerce.orders;
```

The verification step is part of the answer. The post-change plan should show an index access path that can satisfy the pending predicate and recent ordering with far fewer buffers. If the query is written as lower(status) = 'pending', or as status <> 'delivered', the partial-index predicate may not match. That failure is not PostgreSQL being stubborn; it is the planner refusing to assume a condition that is not guaranteed by the query text and available constraints.

For JSONB, the same workflow applies with a different access method:

```sql
CREATE INDEX events_payload_gin_path_idx
ON events.events USING gin (payload jsonb_path_ops);
ANALYZE events.events;
```

A containment predicate such as payload @> '{"phase": 7, "severity": "warning"}' can now be tested before and after the index. If the query extracts a text value with payload ->> 'severity' and compares it with equality, the containment-oriented GIN index may not help. The index has to match the operator family used by the query.

## Diagnostic Questions

Ask these questions before accepting an index design. What is the exact predicate or operator that must become faster? How many rows match it, both as an estimate and as actual rows? Is the data distribution skewed, correlated with insertion order, or mostly uniform? Does the proposed index make writes, vacuum, or autovacuum materially more expensive? Does the query predicate imply the partial-index WHERE clause exactly enough for the planner to use it? Does the expression in the query match the expression in the index? Is a GIN, GiST, or BRIN index being chosen because the data type and operator demand it, or because the index name sounds advanced?

When estimates are badly wrong, do not jump directly to forcing a plan. PostgreSQL does not support optimizer hints in core, and this course treats that as a design signal. Run ANALYZE. Inspect whether columns are correlated. Consider extended statistics with CREATE STATISTICS when a combination of columns is misestimated because single-column histograms miss the relationship. A plan with estimated rows of 10 and actual rows of 200000 is a statistics problem before it is an index problem.

## Common Pitfalls

The common failure is adding a specialized index without a workload. Partial indexes fail when the predicate in production is broader than the predicate in the index, when the rare value stops being rare, or when a prepared statement hides constants in a way that prevents implication. Expression indexes fail when applications apply inconsistent normalization, such as lower(email) in one path and email ILIKE in another. GIN indexes fail as a tradeoff when updates are frequent, pending lists grow, and the query volume does not justify the maintenance. GiST range indexes fail when the query can use a simpler scalar B-tree predicate. BRIN fails when the table is randomly updated or physically uncorrelated with the filtered column.

Another pitfall is reading EXPLAIN as a scoreboard. Lower estimated cost is not proof by itself, and an index scan is not always better than a sequential scan. The plan must be read with rows, loops, buffers, and timing. A Bitmap Heap Scan can be exactly right when many matching tuples are scattered across heap pages. An Index Only Scan may still fetch heap pages when the visibility map is not favorable. A sequential scan over a small table can be ideal.

## Explain It Back

Explain the index as a contract between query and data. For BRIN for Append Heavy Chronological Data, name the query pattern, the data distribution, the access method, and the maintenance cost. Then show the proof using EXPLAIN ANALYZE BUFFERS. If the proof depends on estimates, state whether the estimates match actual rows. If they do not, propose ANALYZE, extended statistics, or a query rewrite before adding more indexes.

A strong answer sounds operational: "The dashboard reads rare pending orders by recent time. The partial index contains only pending rows ordered by placed_at, so the planner can avoid scanning delivered rows and can stop early for the LIMIT. It costs one extra index entry only for rows that enter the pending state, not for every delivered order. I verified it by comparing buffers and actual rows before and after." That is the level of reasoning Phase 7b expects.

## References and Further Reading

Use `docs/indexing-playbook-part2.md` as the local reference for partial, expression, GIN, GiST, and BRIN choices. Keep `docs/indexing-playbook-part1.md` nearby for B-tree, composite, covering, and access-path fundamentals. PostgreSQL's official documentation on indexes, operator classes, EXPLAIN, and planner statistics is the external reference set, but the lab proof is the source of truth for each exercise.
