# A5 Monitoring and Performance Operations Playbook

Monitoring is the evidence layer for PostgreSQL operations. Use `pg_stat_statements` for workload ranking, `pg_stat_activity` and `pg_blocking_pids()` for current blocking, `pg_stat_user_indexes` for index review, table-size queries for capacity, and wait events for fast classification.

Weekly rhythm:

1. Run `pgfound ops query top-by-total-time` and record the top 5 by total time.
2. Compare average time and shared reads against the prior week.
3. Pick one regression candidate and capture `EXPLAIN (ANALYZE, BUFFERS)`.
4. Check table churn and statistics freshness before changing indexes.
5. Write the next verification query before applying the change.

Useful alerts include context. A checkpoint alert should distinguish normal checkpoint spikes from sustained write pressure, include the dashboard link or query, and include a sentence beginning with `what should I do if this fires`.
