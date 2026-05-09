-- domain: scheduling
-- phase: 03
-- depends: phase-02
-- description: appointment status reference table and scheduling invariants

CREATE SCHEMA IF NOT EXISTS scheduling;

CREATE TABLE IF NOT EXISTS scheduling.appointment_statuses (
    code text PRIMARY KEY,
    label text NOT NULL UNIQUE,
    is_terminal boolean NOT NULL DEFAULT false
);

INSERT INTO scheduling.appointment_statuses (code, label, is_terminal)
VALUES
    ('scheduled', 'Scheduled', false),
    ('completed', 'Completed', true),
    ('cancelled', 'Cancelled', true)
ON CONFLICT (code) DO NOTHING;

-- In phase 2, status was free text. In phase 3 we keep the column but bind it
-- to a reference table, so a typo like "schedueld" is rejected by PostgreSQL.
ALTER TABLE scheduling.providers
    ALTER COLUMN display_name SET NOT NULL,
    ALTER COLUMN specialty SET NOT NULL;

ALTER TABLE scheduling.clients
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN full_name SET NOT NULL;

ALTER TABLE scheduling.appointments
    ALTER COLUMN provider_id SET NOT NULL,
    ALTER COLUMN client_id SET NOT NULL,
    ALTER COLUMN starts_at SET NOT NULL,
    ALTER COLUMN ends_at SET NOT NULL,
    ALTER COLUMN status SET DEFAULT 'scheduled',
    ALTER COLUMN status SET NOT NULL;

ALTER TABLE scheduling.availability_blocks
    ALTER COLUMN provider_id SET NOT NULL,
    ALTER COLUMN starts_at SET NOT NULL,
    ALTER COLUMN ends_at SET NOT NULL,
    ALTER COLUMN location SET NOT NULL;

DO $$
BEGIN
    ALTER TABLE scheduling.clients
        ADD CONSTRAINT clients_email_unique UNIQUE (email);
EXCEPTION
    WHEN duplicate_table OR duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE scheduling.appointments
        ADD CONSTRAINT appointments_provider_starts_at_unique UNIQUE (provider_id, starts_at);
EXCEPTION
    WHEN duplicate_table OR duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE scheduling.appointments
        ADD CONSTRAINT appointments_starts_before_ends CHECK (starts_at < ends_at);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE scheduling.availability_blocks
        ADD CONSTRAINT availability_blocks_starts_before_ends CHECK (starts_at < ends_at);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE scheduling.appointments
        ADD CONSTRAINT appointments_status_fkey
        FOREIGN KEY (status) REFERENCES scheduling.appointment_statuses(code);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;
