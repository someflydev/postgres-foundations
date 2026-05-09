# Solution

The missing invariant is that a professional cannot hold two appointments at the same starting instant, and a business identifier can be unique even when it is not the primary key. Without this constraint, an incident could occur when two booking clients reserve the same provider slot and both receive confirmations.

A concrete repair is:

```sql
ALTER TABLE scheduling.appointments
    ALTER COLUMN provider_id SET NOT NULL,
    ALTER COLUMN starts_at SET NOT NULL;

ALTER TABLE scheduling.appointments
    ADD CONSTRAINT appointments_provider_starts_at_unique
    UNIQUE (provider_id, starts_at);
```

If either column were nullable, PostgreSQL uniqueness would still allow multiple rows with NULL in the combination. That is why the NOT NULL tightening is part of the repair.
