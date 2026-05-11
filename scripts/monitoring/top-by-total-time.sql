-- Purpose: rank normalized statements by total runtime, average runtime, and read I/O for weekly triage.
-- Run with: pgfound ops query top-by-total-time
SELECT
    queryid,
    calls,
    round(total_exec_time::numeric, 2) AS total_exec_time_ms,
    round(mean_exec_time::numeric, 2) AS mean_exec_time_ms,
    shared_blks_read,
    shared_blks_hit,
    left(regexp_replace(query, '\s+', ' ', 'g'), 160) AS query_sample
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
