EXPLAIN
SELECT count(*)
FROM events.event_log_partitioned
WHERE event_time >= '2025-11-01'::timestamptz
  AND event_time < '2025-12-01'::timestamptz;
