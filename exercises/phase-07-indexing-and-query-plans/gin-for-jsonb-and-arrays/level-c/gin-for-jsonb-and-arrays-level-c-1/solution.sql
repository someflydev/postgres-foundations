DROP INDEX IF EXISTS events.events_payload_gin_path_idx;
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, event_type, occurred_at
FROM events.events
WHERE payload @> '{"phase": 7, "severity": "warning"}'::jsonb;
CREATE INDEX events_payload_gin_path_idx
ON events.events USING gin (payload jsonb_path_ops);
ANALYZE events.events;
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, event_type, occurred_at
FROM events.events
WHERE payload @> '{"phase": 7, "severity": "warning"}'::jsonb;
