-- domain: event_heavy_ops
-- phase: 05
-- depends: phase-04b
-- expected rows: >= 50000 generated events across at least 5 sources
-- description: bounded append-heavy event volume for expressive querying drills

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS events;

INSERT INTO events.sources (source_key, service_name, environment)
VALUES
    ('checkout-prod', 'checkout', 'prod'),
    ('billing-prod', 'billing', 'prod'),
    ('catalog-prod', 'catalog', 'prod'),
    ('identity-prod', 'identity', 'prod'),
    ('notifications-prod', 'notifications', 'prod')
ON CONFLICT (source_key) DO UPDATE
SET service_name = EXCLUDED.service_name,
    environment = EXCLUDED.environment,
    updated_at = now();

WITH source_map AS (
    SELECT id, row_number() OVER (ORDER BY source_key) AS source_rn
    FROM events.sources
    WHERE source_key IN ('checkout-prod', 'billing-prod', 'catalog-prod', 'identity-prod', 'notifications-prod')
), generated AS (
    SELECT gs,
           ((gs - 1) % 5) + 1 AS source_rn,
           (substr(md5('phase5-event-' || gs), 1, 8) || '-' ||
            substr(md5('phase5-event-' || gs), 9, 4) || '-' ||
            substr(md5('phase5-event-' || gs), 13, 4) || '-' ||
            substr(md5('phase5-event-' || gs), 17, 4) || '-' ||
            substr(md5('phase5-event-' || gs), 21, 12))::uuid AS event_uuid,
           '2026-02-01 00:00:00+00'::timestamptz + ((gs % 43200) * interval '1 minute') AS occurred_at,
           CASE WHEN gs % 19 = 0 THEN 'error'
                WHEN gs % 7 = 0 THEN 'retry'
                WHEN gs % 5 = 0 THEN 'job_completed'
                ELSE 'request_seen' END AS event_type
    FROM generate_series(1, 50000) AS gs
)
INSERT INTO events.events (event_uuid, source_id, event_type, occurred_at, payload)
SELECT g.event_uuid, s.id, g.event_type, g.occurred_at,
       jsonb_build_object('sequence', g.gs, 'phase', 5, 'latency_ms', 20 + (g.gs % 400))
FROM generated g
JOIN source_map s ON s.source_rn = g.source_rn
ON CONFLICT (event_uuid) DO NOTHING;
