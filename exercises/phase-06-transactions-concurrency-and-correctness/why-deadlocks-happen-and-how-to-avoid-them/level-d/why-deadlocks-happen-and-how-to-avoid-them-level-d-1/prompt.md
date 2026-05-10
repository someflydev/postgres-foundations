# Repair Opposite-Order Transfer Functions

Use the Phase 6 seed data to practice Why Deadlocks Happen and How to Avoid Them. Work in psql and keep notes about the session ordering, lock behavior, and invariant being protected.

## Given

The seed data includes Phase 6 rows for ecommerce inventory, order reservations, scheduling holds, and optional bank account transfer drills. Exercise id: `why-deadlocks-happen-and-how-to-avoid-them-level-d-1`.

## Task

A deadlock arises from two functions that update the same two rows in opposite orders. Reorder the work and explain the retry boundary.

For `--check`, submit only the Session B row-locking query that locks both `pgfound_harness.accounts` rows in deterministic id order.

## Success Criteria

- The answer names the invariant before choosing a PostgreSQL mechanism.
- The answer distinguishes the behavior of each session.
- The answer explains why the final state is correct under concurrent load.

## Oral Defense

- Which read or predicate made the decision unsafe?
- Which PostgreSQL behavior did you observe directly?
- What retry, timeout, or lock-ordering rule belongs in application code?
