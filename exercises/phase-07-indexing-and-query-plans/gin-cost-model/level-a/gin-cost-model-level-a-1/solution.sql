CREATE INDEX IF NOT EXISTS events_payload_gin_idx
ON events.events USING gin (payload);
ANALYZE events.events;
EXPLAIN (ANALYZE, BUFFERS)
SELECT id
FROM events.events
WHERE payload @> '{"service": "checkout"}'::jsonb;
