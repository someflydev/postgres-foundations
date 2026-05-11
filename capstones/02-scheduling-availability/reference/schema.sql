CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE practices (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL UNIQUE,
    region text NOT NULL
);

CREATE TABLE professionals (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    practice_id uuid NOT NULL REFERENCES practices(id) ON DELETE CASCADE,
    display_name text NOT NULL,
    timezone text NOT NULL,
    specialties text[] NOT NULL DEFAULT '{}',
    bio text NOT NULL DEFAULT '',
    search_vector tsvector NOT NULL DEFAULT ''::tsvector
);

CREATE TABLE patients (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name text NOT NULL,
    email text NOT NULL UNIQUE
);

CREATE TABLE availability_templates (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    professional_id uuid NOT NULL REFERENCES professionals(id) ON DELETE CASCADE,
    day_of_week integer NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    local_windows tsmultirange NOT NULL,
    effective_during daterange NOT NULL,
    CHECK (NOT isempty(local_windows))
);

CREATE TABLE blackout_windows (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    professional_id uuid NOT NULL REFERENCES professionals(id) ON DELETE CASCADE,
    slot tstzrange NOT NULL,
    reason text NOT NULL,
    CHECK (lower(slot) < upper(slot))
);

CREATE TABLE appointments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    professional_id uuid NOT NULL REFERENCES professionals(id) ON DELETE CASCADE,
    patient_id uuid NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    slot tstzrange NOT NULL,
    status text NOT NULL CHECK (status IN ('confirmed', 'cancelled', 'completed', 'no_show')),
    booked_at timestamptz NOT NULL DEFAULT now(),
    cancelled_at timestamptz,
    CHECK (lower(slot) < upper(slot)),
    EXCLUDE USING gist (
        professional_id WITH =,
        slot WITH &&
    ) WHERE (status = 'confirmed')
);

CREATE TABLE waitlist_entries (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    professional_id uuid NOT NULL REFERENCES professionals(id) ON DELETE CASCADE,
    patient_id uuid NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    desired_slot tstzrange,
    status text NOT NULL DEFAULT 'waiting' CHECK (status IN ('waiting', 'offered', 'booked', 'expired')),
    created_at timestamptz NOT NULL DEFAULT now()
);
