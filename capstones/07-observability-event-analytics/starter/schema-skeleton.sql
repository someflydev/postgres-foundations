CREATE SCHEMA IF NOT EXISTS observability;

CREATE TABLE observability.events (
    event_id bigserial,
    service_name text NOT NULL,
    event_time timestamptz NOT NULL,
    severity text NOT NULL
) PARTITION BY RANGE (event_time);
