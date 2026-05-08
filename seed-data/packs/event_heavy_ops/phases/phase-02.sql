-- domain: event_heavy_ops
-- phase: 02
-- depends: phase-01
-- description: incident links for event joins

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS events;

CREATE TABLE IF NOT EXISTS events.incident_events (
    id bigint generated always as identity PRIMARY KEY,
    incident_key text NOT NULL,
    event_id bigint NOT NULL REFERENCES events.events(id),
    severity text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (incident_key, event_id)
);

INSERT INTO events.incident_events (incident_key, event_id, severity)
VALUES
    (
        'INC-42',
        (SELECT id FROM events.events WHERE event_uuid = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa2'),
        'warning'
    )
ON CONFLICT (incident_key, event_id) DO NOTHING;
