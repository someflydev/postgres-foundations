-- domain: scheduling
-- phase: 06
-- depends: phase-05
-- expected rows: appointment hold rows for double-booking drills
-- description: transaction and range-check practice for scheduling races

CREATE SCHEMA IF NOT EXISTS scheduling;

CREATE TABLE IF NOT EXISTS scheduling.appointment_holds (
    id bigint generated always as identity PRIMARY KEY,
    professional_id bigint NOT NULL REFERENCES scheduling.professionals(id),
    hold_expires_at timestamptz NOT NULL,
    slot tstzrange NOT NULL,
    idempotency_key text UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT appointment_holds_nonempty_check CHECK (NOT isempty(slot))
);

CREATE INDEX IF NOT EXISTS appointment_holds_slot_gist
ON scheduling.appointment_holds
USING gist (slot);

INSERT INTO scheduling.appointment_holds (
    professional_id,
    hold_expires_at,
    slot,
    idempotency_key
)
VALUES
    (
        (SELECT id FROM scheduling.professionals WHERE display_name = 'Dr. Rivera'),
        '2026-05-10 15:10:00+00',
        tstzrange('2026-05-10 15:00:00+00', '2026-05-10 15:30:00+00', '[)'),
        'phase6-existing-hold'
    )
ON CONFLICT (idempotency_key) DO NOTHING;
