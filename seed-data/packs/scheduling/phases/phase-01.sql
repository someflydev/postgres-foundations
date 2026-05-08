-- domain: scheduling
-- phase: 01
-- depends: none
-- description: minimal schema + small seed

CREATE SCHEMA IF NOT EXISTS scheduling;

CREATE TABLE IF NOT EXISTS scheduling.providers (
    id bigint generated always as identity PRIMARY KEY,
    display_name text NOT NULL UNIQUE,
    specialty text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scheduling.clients (
    id bigint generated always as identity PRIMARY KEY,
    email text NOT NULL UNIQUE,
    full_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scheduling.appointments (
    id bigint generated always as identity PRIMARY KEY,
    provider_id bigint NOT NULL REFERENCES scheduling.providers(id),
    client_id bigint NOT NULL REFERENCES scheduling.clients(id),
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    status text NOT NULL DEFAULT 'scheduled',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (provider_id, starts_at)
);

INSERT INTO scheduling.providers (display_name, specialty)
VALUES
    ('Dr. Rivera', 'physical therapy'),
    ('Dr. Chen', 'nutrition')
ON CONFLICT (display_name) DO NOTHING;

INSERT INTO scheduling.clients (email, full_name)
VALUES
    ('sam@example.com', 'Sam Carter'),
    ('nora@example.com', 'Nora Patel')
ON CONFLICT (email) DO NOTHING;

INSERT INTO scheduling.appointments (provider_id, client_id, starts_at, ends_at, status)
VALUES
    (
        (SELECT id FROM scheduling.providers WHERE display_name = 'Dr. Rivera'),
        (SELECT id FROM scheduling.clients WHERE email = 'sam@example.com'),
        '2026-02-10 15:00:00+00',
        '2026-02-10 15:45:00+00',
        'scheduled'
    ),
    (
        (SELECT id FROM scheduling.providers WHERE display_name = 'Dr. Chen'),
        (SELECT id FROM scheduling.clients WHERE email = 'nora@example.com'),
        '2026-02-11 17:00:00+00',
        '2026-02-11 17:30:00+00',
        'scheduled'
    )
ON CONFLICT (provider_id, starts_at) DO NOTHING;
