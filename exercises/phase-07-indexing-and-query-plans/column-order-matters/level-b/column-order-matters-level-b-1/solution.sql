-- Run with pgfound lab explain and compare estimated rows, actual rows, and buffers.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, starts_at, ends_at, status
FROM scheduling.appointments
WHERE provider_id = 1
  AND starts_at >= '2026-01-01'::timestamptz
ORDER BY starts_at
LIMIT 30;
