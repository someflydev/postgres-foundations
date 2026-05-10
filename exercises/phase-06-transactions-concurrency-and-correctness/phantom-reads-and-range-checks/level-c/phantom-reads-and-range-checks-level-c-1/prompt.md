# Trace a Phantom Range Check

Use the Phase 6 seed data to practice Phantom Reads and Range Checks. Work in psql and keep notes about the session ordering, lock behavior, and invariant being protected.

## Given

The seed data includes Phase 6 rows for ecommerce inventory, order reservations, scheduling holds, and optional bank account transfer drills. Exercise id: `phantom-reads-and-range-checks-level-c-1`.

## Task

Show how two sessions can both pass an absence check before inserting overlapping range facts.

For `--check`, submit only the absence-check query against `pgfound_harness.appointment_holds`; it must return one column named `overlapping`.

## Success Criteria

- The answer names the invariant before choosing a PostgreSQL mechanism.
- The answer distinguishes the behavior of each session.
- The answer explains why the final state is correct under concurrent load.

## Oral Defense

- Which read or predicate made the decision unsafe?
- Which PostgreSQL behavior did you observe directly?
- What retry, timeout, or lock-ordering rule belongs in application code?
