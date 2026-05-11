SELECT queryid, calls, round(total_exec_time::numeric, 2) AS total_ms,
       round(mean_exec_time::numeric, 2) AS mean_ms,
       shared_blks_read, shared_blks_hit, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
