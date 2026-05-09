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
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO scheduling.providers (display_name, specialty)
VALUES
    ('Dr. Malik', 'sports medicine')
ON CONFLICT (display_name) DO NOTHING;

INSERT INTO scheduling.clients (email, full_name)
VALUES
    ('lee@example.com', 'Lee Morgan')
ON CONFLICT (email) DO NOTHING;

INSERT INTO scheduling.appointments (provider_id, client_id, starts_at, ends_at, status)
VALUES
    (
        (SELECT id FROM scheduling.providers WHERE display_name = 'Dr. Chen'),
        (SELECT id FROM scheduling.clients WHERE email = 'lee@example.com'),
        '2026-02-13 18:00:00+00',
        '2026-02-13 18:30:00+00',
        'scheduled'
    )
ON CONFLICT (provider_id, starts_at) DO NOTHING;

INSERT INTO scheduling.availability_blocks (provider_id, starts_at, ends_at, location)
SELECT p.id, block.starts_at::timestamptz, block.ends_at::timestamptz, block.location
FROM (
    VALUES
        ('Dr. Rivera', '2026-02-10 14:00:00+00', '2026-02-10 18:00:00+00', 'clinic-a'),
        ('Dr. Chen', '2026-02-11 16:00:00+00', '2026-02-11 19:00:00+00', 'clinic-b'),
        ('Dr. Malik', '2026-02-12 14:00:00+00', '2026-02-12 17:00:00+00', 'clinic-c')
) AS block(display_name, starts_at, ends_at, location)
INNER JOIN scheduling.providers p ON p.display_name = block.display_name
WHERE NOT EXISTS (
    SELECT 1
    FROM scheduling.availability_blocks existing
    WHERE existing.provider_id = p.id
      AND existing.starts_at = block.starts_at::timestamptz
      AND existing.ends_at = block.ends_at::timestamptz
      AND existing.location = block.location
);
