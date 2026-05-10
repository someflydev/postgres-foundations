# Compare Row Lock Strength in Two Sessions

Use the Phase 6 seed data to practice SELECT FOR UPDATE vs FOR NO KEY UPDATE. Work in psql and keep notes about the session ordering, lock behavior, and invariant being protected.

## Given

The seed data includes Phase 6 rows for ecommerce inventory, order reservations, scheduling holds, and optional bank account transfer drills. Exercise id: `select-for-update-vs-for-no-key-update-level-c-2`.

## Task

Trace blocking behavior for FOR UPDATE and FOR NO KEY UPDATE around a reservation row.

For `--check`, submit only the SQL statement that Session A should run after `BEGIN` to lock `pgfound_harness.inventory` row `product_id = 1`.

## Success Criteria

- The answer names the invariant before choosing a PostgreSQL mechanism.
- The answer distinguishes the behavior of each session.
- The answer explains why the final state is correct under concurrent load.

## Oral Defense

- Which read or predicate made the decision unsafe?
- Which PostgreSQL behavior did you observe directly?
- What retry, timeout, or lock-ordering rule belongs in application code?
