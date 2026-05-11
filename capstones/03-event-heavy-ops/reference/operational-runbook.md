# Slow Query Runbook

1. Confirm the query includes an `event_time` range that can prune partitions.
2. Run `EXPLAIN (ANALYZE, BUFFERS)` against the exact query shape.
3. Check whether the plan uses the expected monthly partition and whether the
   device predicate can use the per-partition btree index.
4. Inspect `pg_stat_statements` for mean time, calls, rows, and variance.
5. If the issue is a dashboard aggregate, test a narrower window before adding a
   new index or replica.
6. If retention maintenance is involved, verify no detached partition remains in
   hot query paths and that archive bookkeeping exists.
