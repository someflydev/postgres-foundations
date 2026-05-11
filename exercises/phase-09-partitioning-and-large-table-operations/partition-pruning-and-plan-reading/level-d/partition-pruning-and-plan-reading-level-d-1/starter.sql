EXPLAIN SELECT count(*) FROM events.event_log_partitioned WHERE date_trunc('month', event_time) = '2026-01-01'::timestamptz;
