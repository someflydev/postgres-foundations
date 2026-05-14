# BRIN for Append Heavy Chronological Data

## Problem Framing

BRIN indexes are for very large tables where physical order carries useful information. They do not point to individual rows like B-tree indexes. They summarize ranges of heap pages. That makes them tiny and cheap to maintain, but only selective when the filtered column is physically correlated with table order. Event-heavy systems often have this shape because rows arrive in time order and queries filter by recent or historical time windows.

The learner's job is to recognize when a small summary index is enough. If a table has hundreds of millions of append-only events and most queries filter on `occurred_at`, a BRIN index may be the right first index. If old rows are randomly updated, backfilled out of order, or queried by high-cardinality equality, BRIN may disappoint. The access method is useful because of physical correlation, not because chronological data sounds large.

## Minimal Concept Introduction

A BRIN index stores minimum and maximum values for blocks of table pages. When a query asks for a time range, PostgreSQL can skip page ranges whose summaries cannot contain matching values. If the heap is ordered by `occurred_at`, the skipped ranges can be huge. If the heap is physically scrambled, almost every page range may overlap the filter and the index becomes less useful.

BRIN is especially attractive when a B-tree would be enormous and expensive to maintain. It is not a precision tool. It narrows the scan; it does not usually return a tiny exact set by itself. The after plan may still include rechecks or heap reads. The proof is that buffers and runtime fall enough for the workload.

## Worked Example

Worked example anchor: append-heavy-events-occurred-at-brin

An event-heavy operations table stores millions of events in insertion order. Investigators usually ask for a time window:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, occurred_at, event_type, severity
FROM events.events
WHERE occurred_at >= now() - interval '6 hours'
  AND occurred_at < now()
ORDER BY occurred_at DESC;
```

A B-tree on `occurred_at` may work, but it can be large relative to the query benefit. A BRIN index tests whether summaries are enough:

```sql
CREATE INDEX events_occurred_at_brin_idx
ON events.events USING brin (occurred_at);
ANALYZE events.events;
```

Then compare plans. A useful BRIN plan should skip older page ranges and show a major buffer reduction. It may use a Bitmap Heap Scan with lossy pages. That is not a failure by itself; it is how BRIN often trades precision for size. The answer must include whether the table is still physically correlated with `occurred_at`.

A quick correlation check can start with statistics:

```sql
SELECT attname, correlation
FROM pg_stats
WHERE schemaname = 'events'
  AND tablename = 'events'
  AND attname = 'occurred_at';
```

High positive correlation supports the BRIN story. Low or negative correlation means the physical layout no longer matches time order, and the learner should be skeptical.

## Diagnostic Questions

Ask whether the table is append-heavy or randomly updated. Ask whether the filter is a range over a column correlated with heap order. Ask how large the table and candidate B-tree would be. Ask whether `pages_per_range` should be adjusted for the table size and query windows. Ask whether partitioning is a future answer for retention, while BRIN is a present answer for scanning within large chronological storage.

Also ask whether the query needs recent rows ordered by time with a small limit. Sometimes a B-tree on `occurred_at DESC` may beat BRIN for that query. BRIN wins when the cheap summary is good enough for broad time windows and the table size makes precision indexes expensive.

## Common Pitfalls

The first pitfall is using BRIN on a column with no physical correlation. The second is expecting a BRIN index to behave like a B-tree seek. The third is ignoring backfills that insert old events at the end of the table and weaken summaries. The fourth is keeping BRIN as the only plan for a query that needs selective equality or top-N ordering. The fifth is treating BRIN as a replacement for retention and partitioning; it can complement those designs, not erase them.

## Explain It Back

A good explanation says: "The events table is append-heavy, and `occurred_at` tracks physical order. BRIN stores page-range summaries, so a time-window query can skip most old page ranges with a tiny index. I verified buffers before and after and checked physical correlation. If backfills scramble the heap or queries need tiny top-N lookups, I would consider a B-tree or partitioning instead." That is the practical BRIN argument.

## References and Further Reading

Use `docs/indexing-playbook-part2.md` and `docs/partitioning-playbook.md` when deciding how BRIN fits large chronological tables and future retention work.
