-- domain: scheduling
-- phase: 04b
-- depends: phase-04a
-- description: range and multirange availability modeling examples

CREATE SCHEMA IF NOT EXISTS scheduling;

ALTER TABLE scheduling.professionals
    ADD COLUMN IF NOT EXISTS working_hours tstzmultirange NOT NULL DEFAULT '{}'::tstzmultirange;

UPDATE scheduling.professionals
SET working_hours = CASE display_name
    WHEN 'Dr. Rivera' THEN '{["2026-02-10 14:00:00+00","2026-02-10 22:00:00+00"),["2026-02-11 14:00:00+00","2026-02-11 22:00:00+00")}'::tstzmultirange
    WHEN 'Dr. Chen' THEN '{["2026-02-10 13:00:00+00","2026-02-10 21:00:00+00"),["2026-02-11 13:00:00+00","2026-02-11 21:00:00+00")}'::tstzmultirange
    ELSE '{["2026-02-10 15:00:00+00","2026-02-10 20:00:00+00")}'::tstzmultirange
END
WHERE working_hours = '{}'::tstzmultirange;

CREATE TABLE IF NOT EXISTS scheduling.availability_slots (
    id bigint generated always as identity PRIMARY KEY,
    professional_id bigint NOT NULL REFERENCES scheduling.professionals(id),
    slot tstzrange NOT NULL,
    source text NOT NULL DEFAULT 'phase_04b_seed',
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (professional_id, slot),
    CONSTRAINT availability_slots_nonempty_check CHECK (NOT isempty(slot))
);

INSERT INTO scheduling.availability_slots (professional_id, slot, source)
VALUES
    (
        (SELECT id FROM scheduling.professionals WHERE display_name = 'Dr. Rivera'),
        tstzrange('2026-02-10 14:00:00+00', '2026-02-10 22:00:00+00', '[)'),
        'working-hours-table'
    ),
    (
        (SELECT id FROM scheduling.professionals WHERE display_name = 'Dr. Rivera'),
        tstzrange('2026-02-11 14:00:00+00', '2026-02-11 22:00:00+00', '[)'),
        'working-hours-table'
    ),
    (
        (SELECT id FROM scheduling.professionals WHERE display_name = 'Dr. Chen'),
        tstzrange('2026-02-10 13:00:00+00', '2026-02-10 21:00:00+00', '[)'),
        'working-hours-table'
    )
ON CONFLICT DO NOTHING;
