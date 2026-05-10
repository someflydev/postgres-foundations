# Observability Intro

This short operator tour exists so Phase 7a indexing lessons can reference
`pg_stat_statements` without turning indexing practice into a monitoring
course.

## What pg_stat_statements Captures

`pg_stat_statements` records normalized statement fingerprints and aggregates
runtime statistics for them. Instead of seeing every literal value, you see a
query shape with counters such as calls, total execution time, mean execution
time, rows, shared blocks read, and shared blocks hit. That makes it useful for
finding repeated expensive query patterns before proposing an index.

It does not explain business intent, and it does not prove an index is correct.
Use it to identify candidates, then reproduce a representative query with
`EXPLAIN (ANALYZE, BUFFERS)` in the lab.

## Top 10 by Total Time

```sql
SELECT query,
       calls,
       total_exec_time,
       mean_exec_time,
       rows,
       shared_blks_hit,
       shared_blks_read
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

Read this as workload evidence. A query with high total time may be frequent,
individually slow, or both. A query with high shared block reads may be doing
real I/O. A query with mostly shared hits may still be CPU-heavy or simply
working from cache.

## Reset Stats

Reset statistics when you want a clean measurement window:

```sql
SELECT pg_stat_statements_reset();
```

Do this deliberately. Resetting removes the accumulated evidence for everyone
using that database. In the local lab this is fine; in production it belongs in
an operator workflow.

## Later Depth

Phase admin work in `PROMPT_33` goes deeper on operational dashboards,
retention windows, baselines, and how query statistics fit with logs and
database health checks.
