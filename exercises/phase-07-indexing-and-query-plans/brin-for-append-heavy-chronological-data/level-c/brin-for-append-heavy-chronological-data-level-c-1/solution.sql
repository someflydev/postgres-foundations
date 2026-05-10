DROP INDEX IF EXISTS events.events_occurred_at_brin_idx;
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*)
FROM events.events
WHERE occurred_at >= '2026-02-10 00:00:00+00'
  AND occurred_at < '2026-02-11 00:00:00+00';
CREATE INDEX events_occurred_at_brin_idx
ON events.events USING brin (occurred_at) WITH (pages_per_range = 32);
ANALYZE events.events;
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*)
FROM events.events
WHERE occurred_at >= '2026-02-10 00:00:00+00'
  AND occurred_at < '2026-02-11 00:00:00+00';
