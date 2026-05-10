# BEGIN, COMMIT, ROLLBACK, and Error Handling Level D1

Use the Phase 6 seed data to practice BEGIN, COMMIT, ROLLBACK, and Error Handling. Work in psql and keep notes about the session ordering, lock behavior, and invariant being protected.

## Given

The seed data includes Phase 6 rows for ecommerce inventory, order reservations, scheduling holds, and optional bank account transfer drills. Exercise id: `begin-commit-rollback-and-error-handling-level-d-1`.

## Task

Analyze the begin, commit, rollback, and error handling scenario and produce the requested Phase 6 outcome.

## Success Criteria

- The answer names the invariant before choosing a PostgreSQL mechanism.
- The answer distinguishes the behavior of each session.
- The answer explains why the final state is correct under concurrent load.

## Oral Defense

- Which read or predicate made the decision unsafe?
- Which PostgreSQL behavior did you observe directly?
- What retry, timeout, or lock-ordering rule belongs in application code?
