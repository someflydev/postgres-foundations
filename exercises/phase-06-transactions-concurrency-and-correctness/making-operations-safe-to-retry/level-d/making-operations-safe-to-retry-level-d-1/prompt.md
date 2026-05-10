# Make Reservation Retry Idempotent

Use the Phase 6 seed data to practice Making Operations Safe to Retry. Work in psql and keep notes about the session ordering, lock behavior, and invariant being protected.

## Given

The seed data includes Phase 6 rows for ecommerce inventory, order reservations, scheduling holds, and optional bank account transfer drills. Exercise id: `making-operations-safe-to-retry-level-d-1`.

## Task

Trace a timeout and retry of the same reservation request, then add an idempotency key so the retry returns the original result.

For `--check`, submit only the retry insert into `pgfound_harness.transfer_requests`; it should use the existing `retry-key` idempotency key and avoid duplicating the transfer.

## Success Criteria

- The answer names the invariant before choosing a PostgreSQL mechanism.
- The answer distinguishes the behavior of each session.
- The answer explains why the final state is correct under concurrent load.

## Oral Defense

- Which read or predicate made the decision unsafe?
- Which PostgreSQL behavior did you observe directly?
- What retry, timeout, or lock-ordering rule belongs in application code?
