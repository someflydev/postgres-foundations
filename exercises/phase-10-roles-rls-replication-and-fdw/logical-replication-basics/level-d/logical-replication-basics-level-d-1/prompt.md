# Logical Replication Basics Level D1

## Setup

Use the logical replication profile from Phase 10.

## Task

Diagnose this incident: inserts on the publisher eventually arrive, so the team
says replication is "working," but lag grows without bound and the publisher's
storage keeps increasing. The subscription slot is active only intermittently,
and an unvacuumable catalog table points to old replication state being
retained.

Write the SQL observations and the repair plan.

## Success Criteria

- Checks subscription status and publisher slot state.
- Explains why a working subscription can still create unbounded lag.
- Names a safe cleanup or recovery sequence before dropping any slot.
