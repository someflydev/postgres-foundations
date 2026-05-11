# E1 pg_stat_statements

`pg_stat_statements` is the workload ledger for repeated SQL. Use it to rank normalized statements by total time, mean time, calls, rows, and I/O counters, then move into `EXPLAIN (ANALYZE, BUFFERS)` for representative query shapes.

Operational rules:

- Confirm `shared_preload_libraries=pg_stat_statements` before expecting rows.
- Set `pg_stat_statements.max` high enough for the workload; too low cycles entries and hides pain.
- Enable `track_io_timing` when I/O timing matters enough to pay the measurement cost.
- Reset only at deliberate baseline boundaries, not during an incident where evidence is still needed.
- Treat query normalization as useful but imperfect for dynamic SQL, large `IN` lists, and JSONB path-heavy statements.
