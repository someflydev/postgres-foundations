CREATE EXTENSION IF NOT EXISTS pg_partman;

CREATE SCHEMA IF NOT EXISTS observability;

CREATE TABLE observability.events (
    event_id bigserial,
    trace_id uuid NOT NULL,
    service_name text NOT NULL,
    event_time timestamptz NOT NULL,
    severity text NOT NULL CHECK (severity IN ('debug', 'info', 'warn', 'error')),
    latency_ms integer,
    attributes jsonb NOT NULL DEFAULT '{}'::jsonb,
    PRIMARY KEY (event_id, event_time)
) PARTITION BY RANGE (event_time);

CREATE TABLE observability.events_2026_05_12
PARTITION OF observability.events
FOR VALUES FROM ('2026-05-12') TO ('2026-05-13');

CREATE TABLE observability.service_hourly_rollups (
    service_name text NOT NULL,
    bucket_start timestamptz NOT NULL,
    event_count bigint NOT NULL,
    p95_latency_ms numeric,
    PRIMARY KEY (service_name, bucket_start)
);
