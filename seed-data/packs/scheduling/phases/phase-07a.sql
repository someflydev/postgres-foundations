-- domain: scheduling
-- phase: 07a
-- depends: phase-06
-- expected rows: >= 50k appointments across 10 professionals after generated COPY load
-- description: dense appointment history for scan, B-tree, and composite-index planning labs

CREATE SCHEMA IF NOT EXISTS scheduling;

INSERT INTO scheduling.providers (display_name, specialty, timezone)
VALUES
    ('Dr. Rivera', 'physical therapy', 'America/Chicago'),
    ('Dr. Chen', 'nutrition', 'America/New_York'),
    ('Dr. Malik', 'sports medicine', 'America/Denver'),
    ('Dr. Alvarez', 'orthopedics', 'America/Chicago'),
    ('Dr. Brooks', 'sports medicine', 'America/Los_Angeles'),
    ('Dr. Coleman', 'nutrition', 'America/New_York'),
    ('Dr. Diaz', 'physical therapy', 'America/Denver'),
    ('Dr. Evans', 'orthopedics', 'America/Chicago'),
    ('Dr. Foster', 'sports medicine', 'America/Los_Angeles'),
    ('Dr. Gupta', 'nutrition', 'America/New_York')
ON CONFLICT (display_name) DO UPDATE
SET specialty = EXCLUDED.specialty,
    timezone = EXCLUDED.timezone;

INSERT INTO scheduling.professionals (id, display_name, specialty, timezone, created_at, updated_at)
SELECT id, display_name, specialty, timezone, created_at, updated_at
FROM scheduling.providers
WHERE display_name IN (
    'Dr. Rivera',
    'Dr. Chen',
    'Dr. Malik',
    'Dr. Alvarez',
    'Dr. Brooks',
    'Dr. Coleman',
    'Dr. Diaz',
    'Dr. Evans',
    'Dr. Foster',
    'Dr. Gupta'
)
ON CONFLICT (id) DO UPDATE
SET display_name = EXCLUDED.display_name,
    specialty = EXCLUDED.specialty,
    timezone = EXCLUDED.timezone,
    updated_at = now();

CREATE UNLOGGED TABLE IF NOT EXISTS scheduling.phase_07a_clients_stage (
    email text PRIMARY KEY,
    full_name text NOT NULL,
    created_at timestamptz NOT NULL
);

CREATE UNLOGGED TABLE IF NOT EXISTS scheduling.phase_07a_appointments_stage (
    professional_name text NOT NULL,
    client_email text NOT NULL,
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    status text NOT NULL
);

CREATE INDEX IF NOT EXISTS phase_07a_appointments_stage_professional_idx
ON scheduling.phase_07a_appointments_stage (professional_name, starts_at);

CREATE INDEX IF NOT EXISTS phase_07a_appointments_stage_client_idx
ON scheduling.phase_07a_appointments_stage (client_email);
