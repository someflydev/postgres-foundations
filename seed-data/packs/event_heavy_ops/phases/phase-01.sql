-- domain: event_heavy_ops
-- phase: 01
-- depends: none
-- description: minimal schema + small seed

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS events;

CREATE TABLE IF NOT EXISTS events.sources (
    id bigint generated always as identity PRIMARY KEY,
    source_key text NOT NULL UNIQUE,
    service_name text NOT NULL,
    environment text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS events.events (
    id bigint generated always as identity PRIMARY KEY,
    event_uuid uuid NOT NULL DEFAULT gen_random_uuid(),
    source_id bigint NOT NULL REFERENCES events.sources(id),
    event_type text NOT NULL,
    occurred_at timestamptz NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (event_uuid)
);

INSERT INTO events.sources (source_key, service_name, environment)
VALUES
    ('checkout-prod', 'checkout', 'prod'),
    ('billing-prod', 'billing', 'prod')
ON CONFLICT (source_key) DO NOTHING;

INSERT INTO events.events (event_uuid, source_id, event_type, occurred_at, payload)
VALUES
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1',
        (SELECT id FROM events.sources WHERE source_key = 'checkout-prod'),
        'order_placed',
        '2026-03-01 12:00:00+00',
        '{"order_number": "EC-1001"}'
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa2',
        (SELECT id FROM events.sources WHERE source_key = 'billing-prod'),
        'payment_captured',
        '2026-03-01 12:01:30+00',
        '{"order_number": "EC-1001", "amount": 43.50}'
    )
ON CONFLICT (event_uuid) DO NOTHING;
