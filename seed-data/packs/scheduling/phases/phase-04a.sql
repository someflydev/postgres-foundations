-- domain: scheduling
-- phase: 04a
-- depends: phase-03
-- description: tenant UUID preview and time-zone-aware appointment data

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS scheduling;

CREATE OR REPLACE FUNCTION scheduling.is_valid_timezone(candidate text)
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
    SELECT EXISTS (
        SELECT 1
        FROM pg_timezone_names
        WHERE name = candidate
    );
$$;

ALTER TABLE scheduling.providers
    ADD COLUMN IF NOT EXISTS timezone text;

UPDATE scheduling.providers
SET timezone = CASE display_name
    WHEN 'Dr. Rivera' THEN 'America/Chicago'
    WHEN 'Dr. Chen' THEN 'America/New_York'
    WHEN 'Dr. Malik' THEN 'America/Denver'
    ELSE 'UTC'
END
WHERE timezone IS NULL;

ALTER TABLE scheduling.providers
    ALTER COLUMN timezone SET DEFAULT 'UTC',
    ALTER COLUMN timezone SET NOT NULL;

DO $$
BEGIN
    ALTER TABLE scheduling.providers
        ADD CONSTRAINT providers_timezone_valid_check
        CHECK (scheduling.is_valid_timezone(timezone));
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM pg_class c
        INNER JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'scheduling'
          AND c.relname = 'professionals'
          AND c.relkind = 'v'
    ) THEN
        DROP VIEW scheduling.professionals;
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS scheduling.professionals (
    id bigint PRIMARY KEY REFERENCES scheduling.providers(id),
    display_name text NOT NULL UNIQUE,
    specialty text NOT NULL,
    timezone text NOT NULL,
    created_at timestamptz NOT NULL,
    updated_at timestamptz NOT NULL,
    CONSTRAINT professionals_timezone_valid_check
        CHECK (scheduling.is_valid_timezone(timezone))
);

INSERT INTO scheduling.professionals (
    id,
    display_name,
    specialty,
    timezone,
    created_at,
    updated_at
)
SELECT id, display_name, specialty, timezone, created_at, updated_at
FROM scheduling.providers
ON CONFLICT (id) DO UPDATE
SET display_name = EXCLUDED.display_name,
    specialty = EXCLUDED.specialty,
    timezone = EXCLUDED.timezone,
    updated_at = EXCLUDED.updated_at;

ALTER TABLE scheduling.appointments
    ADD COLUMN IF NOT EXISTS tenant_id uuid;

UPDATE scheduling.appointments
SET tenant_id = CASE
    WHEN provider_id = (SELECT id FROM scheduling.providers WHERE display_name = 'Dr. Rivera')
        THEN 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'::uuid
    WHEN provider_id = (SELECT id FROM scheduling.providers WHERE display_name = 'Dr. Chen')
        THEN 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'::uuid
    ELSE 'cccccccc-cccc-cccc-cccc-cccccccccccc'::uuid
END
WHERE tenant_id IS NULL;

ALTER TABLE scheduling.appointments
    ALTER COLUMN tenant_id SET DEFAULT gen_random_uuid(),
    ALTER COLUMN tenant_id SET NOT NULL;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'scheduling'
          AND table_name = 'appointments'
          AND column_name = 'starts_at'
          AND data_type = 'timestamp without time zone'
    ) THEN
        ALTER TABLE scheduling.appointments
            ALTER COLUMN starts_at TYPE timestamptz USING starts_at AT TIME ZONE 'UTC',
            ALTER COLUMN ends_at TYPE timestamptz USING ends_at AT TIME ZONE 'UTC';
    END IF;
END
$$;
