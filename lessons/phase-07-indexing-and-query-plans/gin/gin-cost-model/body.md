# GIN Cost Model

## Problem Framing

A GIN index can make containment queries dramatically faster, but it can also become one of the most expensive structures in the database. This lesson is about cost, not syntax. Learners should be able to explain build time, write overhead, pending list behavior, vacuum pressure, bloat, and when to say no. The right answer for a write-heavy workload may be a narrower expression index, a relational redesign, or no index yet.

GIN has a distinctive write path. With `fastupdate` enabled, PostgreSQL can buffer new GIN entries in a pending list before merging them into the main index. That can make individual writes cheaper, but a large pending list can shift cost into later reads, vacuum, or cleanup. With `fastupdate` disabled, writes pay more immediately. Neither setting is universally correct. It depends on write rate, read latency requirements, maintenance windows, and the size of the indexed values.

## Minimal Concept Introduction

The cost model starts with workload volume. How many rows are inserted or updated per second? How wide is the JSONB document, array, or tsvector? How often does the indexed query run, and how selective is it? A GIN index with excellent read wins can still be a bad tradeoff if the table is updated constantly and the query is rare. Conversely, a read-heavy support search over mostly stable documents may justify a larger index.

The cost model also includes observability. Learners should inspect index size, query plans, buffers, and maintenance symptoms. They should know that bloat is not only a table problem. Large or churn-heavy GIN indexes can require vacuum attention and reindex planning. The answer must include removal or redesign criteria.

## Worked Example

Worked example anchor: write-heavy-jsonb-gin-pending-list

An incident table receives frequent updates to `payload` as alerts are enriched. A team proposes this index because one dashboard filters warnings:

```sql
CREATE INDEX events_payload_gin_ops_idx
ON events.events USING gin (payload jsonb_ops);
```

Before accepting it, measure both read and maintenance signals:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, occurred_at
FROM events.events
WHERE payload @> '{"severity": "warning"}'::jsonb
ORDER BY occurred_at DESC
LIMIT 100;

SELECT pg_size_pretty(pg_relation_size('events.events'::regclass)) AS table_size,
       pg_size_pretty(pg_relation_size('events_payload_gin_ops_idx'::regclass)) AS index_size;
```

If the dashboard runs every few seconds and warning events are selective, the index may be justified. If it runs twice a day while enrichment updates every row several times, the bloat-to-value ratio is poor. A narrower `jsonb_path_ops` index may be better for containment. A generated severity column plus B-tree may be better if severity is a stable, hot key. If neither read volume nor selectivity is proven, the correct answer is "not yet."

Fastupdate belongs in the discussion:

```sql
ALTER INDEX events_payload_gin_ops_idx SET (fastupdate = off);
```

That statement is not a magic fix. It changes where write cost is paid. Learners should treat it as a tested configuration change with before and after measurements, not a default recommendation.

## Diagnostic Questions

Ask how often the indexed document changes, how many keys or elements each row contributes, and how selective the predicate is. Ask whether `jsonb_ops` is needed or `jsonb_path_ops` is enough. Ask whether pending list cleanup shows up as latency spikes. Ask whether the team has a maintenance window for `REINDEX CONCURRENTLY` if bloat becomes severe. Ask whether a smaller partial GIN index, an expression index, or relational extraction would solve the specific hot predicate with less cost.

## Common Pitfalls

The first pitfall is measuring only the happy read plan. The second is building a wide GIN index on a column that changes on every write. The third is turning off `fastupdate` without measuring write latency and cleanup behavior. The fourth is ignoring common values; if most documents contain the same key, the index may find too many rows to be useful. The fifth is keeping a GIN index after the feature that needed it has moved elsewhere.

## Explain It Back

A strong answer says: "The GIN index matches our containment operator, but this table updates payload frequently. I would compare read buffers and latency against index size, write rate, and pending list behavior. If the query is rare or unselective, I would not keep the index. If severity is the real hot key, I would consider a generated column and B-tree. If containment remains hot, I would choose the narrowest operator class and document reindex and drop criteria." That is a cost model, not an index catalog answer.

## References and Further Reading

Use `docs/indexing-playbook-part2.md` and the GIN sections of PostgreSQL documentation when evaluating `fastupdate`, pending list behavior, and bloat.
