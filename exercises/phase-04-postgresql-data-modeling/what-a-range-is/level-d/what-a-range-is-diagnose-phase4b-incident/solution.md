# Reference Solution

The modeled fact is an appointment slot, not two unrelated timestamps. Keeping
`starts_at` and `ends_at` as the only representation leaves overlap semantics
in application code. Different services can choose different bound behavior,
and two concurrent inserts can pass an app-side pre-check before either row is
visible to the other request.

Use one `tstzrange` value for the slot and an exclusion constraint for the
database invariant:

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE scheduling.appointments
    ADD COLUMN slot tstzrange;

UPDATE scheduling.appointments
SET slot = tstzrange(starts_at, ends_at, '[)')
WHERE slot IS NULL;

ALTER TABLE scheduling.appointments
    ALTER COLUMN slot SET NOT NULL,
    ADD CONSTRAINT appointments_slot_nonempty_check CHECK (NOT isempty(slot)),
    ADD CONSTRAINT appointments_no_provider_overlap
        EXCLUDE USING gist (
            provider_id WITH =,
            slot WITH &&
        );
```

The app may still perform a friendly pre-check to show a useful message, but
the source of truth is PostgreSQL. If an overlapping insert reaches the
database, `slot WITH &&` conflicts with the existing range for the same
provider and PostgreSQL rejects it.
