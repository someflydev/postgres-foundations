-- domain: scheduling
-- phase: 05
-- depends: phase-04b
-- expected rows: >= 1500 generated appointments, at least 500 appointments per 3 professionals
-- description: dense appointment history for windows, CTEs, lateral joins, and gaps

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS scheduling;

INSERT INTO scheduling.providers (display_name, specialty, timezone)
VALUES
    ('Dr. Rivera', 'physical therapy', 'America/Chicago'),
    ('Dr. Chen', 'nutrition', 'America/New_York'),
    ('Dr. Malik', 'sports medicine', 'America/Denver')
ON CONFLICT (display_name) DO UPDATE
SET specialty = EXCLUDED.specialty,
    timezone = EXCLUDED.timezone;

INSERT INTO scheduling.professionals (id, display_name, specialty, timezone, created_at, updated_at)
SELECT id, display_name, specialty, timezone, created_at, updated_at
FROM scheduling.providers
WHERE display_name IN ('Dr. Rivera', 'Dr. Chen', 'Dr. Malik')
ON CONFLICT (id) DO UPDATE
SET display_name = EXCLUDED.display_name,
    specialty = EXCLUDED.specialty,
    timezone = EXCLUDED.timezone,
    updated_at = now();

INSERT INTO scheduling.clients (email, full_name)
SELECT format('phase5-client-%s@example.com', gs), format('Phase Five Client %s', gs)
FROM generate_series(1, 900) AS gs
ON CONFLICT (email) DO NOTHING;

WITH professionals AS (
    SELECT id, row_number() OVER (ORDER BY display_name) AS provider_rn
    FROM scheduling.professionals
    WHERE display_name IN ('Dr. Rivera', 'Dr. Chen', 'Dr. Malik')
), clients AS (
    SELECT id, row_number() OVER (ORDER BY email) AS client_rn
    FROM scheduling.clients
    WHERE email LIKE 'phase5-client-%@example.com'
), generated AS (
    SELECT p.id AS provider_id,
           c.id AS client_id,
           '2025-07-01 13:00:00+00'::timestamptz
             + ((appt_n - 1) * interval '1 day')
             + ((p.provider_rn - 1) * interval '2 hours') AS starts_at,
           CASE WHEN appt_n % 9 = 0 THEN 'cancelled'
                WHEN appt_n < 400 THEN 'completed'
                ELSE 'scheduled' END AS status
    FROM professionals p
    CROSS JOIN generate_series(1, 501) AS appt_n
    JOIN clients c ON c.client_rn = (((appt_n + p.provider_rn * 37 - 1) % 900) + 1)
)
INSERT INTO scheduling.appointments (provider_id, client_id, starts_at, ends_at, status, tenant_id)
SELECT provider_id, client_id, starts_at, starts_at + interval '45 minutes', status,
       ('00000000-0000-0000-0000-' || lpad(provider_id::text, 12, '0'))::uuid
FROM generated
ON CONFLICT (provider_id, starts_at) DO NOTHING;
