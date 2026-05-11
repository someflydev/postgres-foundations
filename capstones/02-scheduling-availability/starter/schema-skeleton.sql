CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE practices (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL
);

CREATE TABLE professionals (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    practice_id uuid NOT NULL REFERENCES practices(id),
    display_name text NOT NULL,
    timezone text NOT NULL
);

-- TODO: add patients, availability templates, blackout windows, appointments,
-- waitlist entries, exclusion constraints, and indexes.
