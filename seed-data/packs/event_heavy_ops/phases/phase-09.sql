-- domain: event_heavy_ops
-- phase: 09
-- depends: phase-07b
-- expected rows: >= 1,000,000 partitioned operational events
-- description: range-partitioned event log, partitioned indexes, and retention via detach

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS events;

DROP TABLE IF EXISTS events.event_log_partitioned CASCADE;
DROP TABLE IF EXISTS events.event_log_partitioned_2025_05 CASCADE;
DROP TABLE IF EXISTS events.event_log_cold_2025_05 CASCADE;

CREATE TABLE events.event_log_partitioned (
    event_id bigint NOT NULL,
    event_uuid uuid NOT NULL,
    source_id bigint NOT NULL REFERENCES events.sources(id),
    event_type text NOT NULL,
    event_time timestamptz NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (event_id, event_time),
    UNIQUE (event_uuid, event_time)
) PARTITION BY RANGE (event_time);

CREATE TABLE events.event_log_partitioned_2025_05 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2025-05-01 00:00:00+00') TO ('2025-06-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2025_06 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2025-06-01 00:00:00+00') TO ('2025-07-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2025_07 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2025-07-01 00:00:00+00') TO ('2025-08-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2025_08 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2025-08-01 00:00:00+00') TO ('2025-09-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2025_09 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2025-09-01 00:00:00+00') TO ('2025-10-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2025_10 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2025-10-01 00:00:00+00') TO ('2025-11-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2025_11 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2025-11-01 00:00:00+00') TO ('2025-12-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2025_12 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2025-12-01 00:00:00+00') TO ('2026-01-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2026_01 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2026-01-01 00:00:00+00') TO ('2026-02-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2026_02 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2026-02-01 00:00:00+00') TO ('2026-03-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2026_03 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2026-03-01 00:00:00+00') TO ('2026-04-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_2026_04 PARTITION OF events.event_log_partitioned
    FOR VALUES FROM ('2026-04-01 00:00:00+00') TO ('2026-05-01 00:00:00+00');
CREATE TABLE events.event_log_partitioned_default PARTITION OF events.event_log_partitioned DEFAULT;

CREATE INDEX event_log_partitioned_event_time_brin
ON events.event_log_partitioned USING brin (event_time);

CREATE INDEX event_log_partitioned_source_id_event_time_idx
ON events.event_log_partitioned (source_id, event_time DESC);

WITH source_map AS (
    SELECT id, row_number() OVER (ORDER BY source_key) AS source_rn
    FROM events.sources
    WHERE source_key IN (
        'billing-prod',
        'catalog-prod',
        'checkout-prod',
        'identity-prod',
        'notifications-prod'
    )
), generated AS (
    SELECT
        gs,
        ((gs - 1) % 5) + 1 AS source_rn,
        '2025-05-01 00:00:00+00'::timestamptz
            + (((gs - 1) % 365) * interval '1 day')
            + (((gs - 1) % 86400) * interval '1 second') AS event_time,
        CASE
            WHEN gs % 37 = 0 THEN 'error'
            WHEN gs % 11 = 0 THEN 'retry'
            WHEN gs % 5 = 0 THEN 'job_completed'
            ELSE 'request_seen'
        END AS event_type
    FROM generate_series(1, 1000008) AS gs
)
INSERT INTO events.event_log_partitioned (
    event_id,
    event_uuid,
    source_id,
    event_type,
    event_time,
    payload,
    created_at
)
SELECT
    g.gs,
    (substr(md5('phase9-event-' || g.gs), 1, 8) || '-' ||
     substr(md5('phase9-event-' || g.gs), 9, 4) || '-' ||
     substr(md5('phase9-event-' || g.gs), 13, 4) || '-' ||
     substr(md5('phase9-event-' || g.gs), 17, 4) || '-' ||
     substr(md5('phase9-event-' || g.gs), 21, 12))::uuid,
    s.id,
    g.event_type,
    g.event_time,
    jsonb_build_object(
        'phase', 9,
        'sequence', g.gs,
        'severity', CASE WHEN g.gs % 37 = 0 THEN 'critical' ELSE 'info' END,
        'service_bucket', g.source_rn
    ),
    g.event_time
FROM generated g
JOIN source_map s ON s.source_rn = g.source_rn;

CREATE TABLE events.event_log_cold_2025_05
AS SELECT * FROM events.event_log_partitioned_2025_05;

ALTER TABLE events.event_log_partitioned
DETACH PARTITION events.event_log_partitioned_2025_05;

COMMENT ON TABLE events.event_log_cold_2025_05
IS 'Detached cold archive created by Phase 9 retention-via-detach seed.';

ANALYZE events.event_log_partitioned;
ANALYZE events.event_log_cold_2025_05;
