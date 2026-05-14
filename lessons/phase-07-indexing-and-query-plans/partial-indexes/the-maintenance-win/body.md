# The Maintenance Win

## Problem Framing

Index design is not only a read-path decision. Every index is also a write-path, vacuum, cache, backup, and restore decision. The maintenance win of a smaller or removed index is often more important than a single faster query. This lesson focuses on that accounting. A learner should be able to explain which indexes earn their keep, which indexes overlap, and which indexes should be dropped because their maintenance cost is larger than their read value.

The danger in advanced indexing is that specialized access paths feel sophisticated. A partial index, expression index, GIN index, GiST index, or BRIN index can all be correct in the right workload. They can also quietly slow inserts, updates, autovacuum, and incident response. The platform doctrine is operational: an index is a contract with a query pattern and a measured benefit, not a trophy.

## Minimal Concept Introduction

Write amplification is the extra work paid when a row change must update table storage plus every affected index. Large indexes also consume shared buffers, lengthen backup and restore time, and give autovacuum more dead entries to clean. A maintenance review therefore starts with two questions: which indexes are scanned, and which indexes are expensive to maintain? PostgreSQL's statistics views, especially `pg_stat_user_indexes`, help find unused indexes. Size functions such as `pg_relation_size` and `pg_size_pretty` help make the cost visible.

The maintenance win can come from a partial index that replaces a broad index, from dropping a redundant index whose leading columns are covered by another index, or from rejecting a proposed GIN index because the write rate is too high for the read benefit. The point is to keep the set small enough that each index has a job.

## Worked Example

Worked example anchor: redundant-order-index-maintenance

Suppose an ecommerce system has accumulated these indexes during several tuning passes:

```sql
CREATE INDEX orders_customer_idx ON ecommerce.orders (customer_id);
CREATE INDEX orders_customer_placed_idx ON ecommerce.orders (customer_id, placed_at DESC);
CREATE INDEX orders_customer_status_idx ON ecommerce.orders (customer_id, status);
```

Before dropping anything, inspect usage and size:

```sql
SELECT
    indexrelname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'ecommerce'
  AND relname = 'orders'
ORDER BY pg_relation_size(indexrelid) DESC;
```

Then connect the candidate index to real queries. If the primary workload is "recent orders for a customer", `(customer_id, placed_at DESC)` may cover the single-column lookup well enough because `customer_id` is the leading column. If no query filters by `(customer_id, status)`, that index may be pure write cost. The safe change is not `DROP INDEX` during a hunch. It is a documented review: capture usage, confirm no known query depends on the candidate, test in staging, and then use `DROP INDEX CONCURRENTLY` in production when appropriate.

## Diagnostic Questions

For each index, ask which query uses it, how often it is scanned, how large it is, and which writes touch it. Ask whether it duplicates another index's leading columns. Ask whether an index-only scan is realistic or whether visibility-map misses still force heap reads. Ask whether a partial index can replace a broad one because only a rare state is operationally hot. Ask whether a BRIN index would be enough for an append-heavy time filter instead of a much larger B-tree.

A maintenance review should also name the rollback path. If a dropped index turns out to matter, how long does a concurrent rebuild take on the production table? Is there enough disk headroom for the rebuild? Are replicas, backups, and maintenance windows accounted for?

## Common Pitfalls

The most common pitfall is treating `idx_scan = 0` as automatic permission to drop. A rarely used index may protect an important monthly close, compliance export, or incident query. The second pitfall is measuring only query latency and ignoring the write path. The third is keeping overlapping indexes because nobody owns removal. The fourth is adding one-off indexes for an emergency and never scheduling the cleanup.

## Explain It Back

A strong answer sounds like an operations review: "This index is 8 GB, has no scans in the observed window, and overlaps with `(customer_id, placed_at DESC)` for our known customer lookup. It adds write amplification to every order insert and update. I would verify the query inventory, test removal in staging, and drop it concurrently with a rebuild plan if a hidden report depends on it." The maintenance win is not abstract tidiness. It is lower write cost, less bloat pressure, smaller backups, and a smaller set of access paths the team can actually reason about.

## References and Further Reading

Use `docs/anti-patterns/unused_indexes.md`, `docs/anti-patterns/redundant_indexes.md`, and `docs/indexing-playbook-part2.md` while reviewing index value and removal criteria.
