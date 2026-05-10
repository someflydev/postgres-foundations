CREATE INDEX IF NOT EXISTS events_created_at_brin_idx
ON events.events USING brin (created_at);
ANALYZE events.events;
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*)
FROM events.events
WHERE created_at >= now() - interval '30 days';
