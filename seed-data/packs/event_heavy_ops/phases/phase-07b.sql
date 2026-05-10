-- domain: event_heavy_ops
-- phase: 07b
-- depends: phase-05
-- expected rows: >= 50000 generated events with richer JSONB payloads
-- description: JSONB, GIN, and BRIN-friendly event payloads for advanced indexing labs

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS events;

UPDATE events.events
SET payload = payload
    || jsonb_build_object(
        'phase', 7,
        'service', CASE source_id % 5
            WHEN 0 THEN 'checkout'
            WHEN 1 THEN 'billing'
            WHEN 2 THEN 'catalog'
            WHEN 3 THEN 'identity'
            ELSE 'notifications'
        END,
        'severity', CASE
            WHEN id % 37 = 0 THEN 'critical'
            WHEN id % 11 = 0 THEN 'warning'
            ELSE 'info'
        END,
        'tags', to_jsonb(ARRAY[
            CASE WHEN id % 2 = 0 THEN 'api' ELSE 'worker' END,
            CASE WHEN id % 7 = 0 THEN 'retry' ELSE 'steady' END
        ])
    ),
    updated_at = greatest(updated_at, occurred_at)
WHERE payload->>'phase' IS DISTINCT FROM '7';

ANALYZE events.events;
ANALYZE events.event_windows;
