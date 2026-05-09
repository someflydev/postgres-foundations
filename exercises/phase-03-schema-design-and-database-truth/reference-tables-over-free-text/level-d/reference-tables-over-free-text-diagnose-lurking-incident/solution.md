# Solution

The missing invariant is that status values must come from a controlled set. Without this constraint, an incident could occur when one writer stores `schedueld`, another stores `scheduled`, and operational reports miss active appointments.

A concrete repair is:

```sql
CREATE TABLE scheduling.appointment_statuses (
    code text PRIMARY KEY,
    label text NOT NULL UNIQUE,
    is_terminal boolean NOT NULL DEFAULT false
);

ALTER TABLE scheduling.appointments
    ALTER COLUMN status SET DEFAULT 'scheduled',
    ALTER COLUMN status SET NOT NULL;

ALTER TABLE scheduling.appointments
    ADD CONSTRAINT appointments_status_fkey
    FOREIGN KEY (status) REFERENCES scheduling.appointment_statuses(code);
```

A reference table stays inspectable, portable, and extensible when the value later needs labels or lifecycle metadata.
