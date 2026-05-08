-- domain: scheduling
-- phase: 02
-- depends: phase-01
-- description: availability blocks for joins and open-slot aggregates

CREATE SCHEMA IF NOT EXISTS scheduling;

CREATE TABLE IF NOT EXISTS scheduling.availability_blocks (
    id bigint generated always as identity PRIMARY KEY,
    provider_id bigint NOT NULL REFERENCES scheduling.providers(id),
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    location text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (provider_id, starts_at)
);

INSERT INTO scheduling.availability_blocks (provider_id, starts_at, ends_at, location)
VALUES
    (
        (SELECT id FROM scheduling.providers WHERE display_name = 'Dr. Rivera'),
        '2026-02-10 14:00:00+00',
        '2026-02-10 18:00:00+00',
        'clinic-a'
    ),
    (
        (SELECT id FROM scheduling.providers WHERE display_name = 'Dr. Chen'),
        '2026-02-11 16:00:00+00',
        '2026-02-11 19:00:00+00',
        'clinic-b'
    )
ON CONFLICT (provider_id, starts_at) DO NOTHING;
