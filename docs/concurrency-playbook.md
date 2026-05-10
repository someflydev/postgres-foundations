# Concurrency Playbook

This page is the Phase 6 reference for the three race families learners must
be able to reproduce, fix, and explain. The goal is not to memorize one magic
lock. The goal is to name the invariant, identify the concurrent reads and
writes, and choose the weakest PostgreSQL mechanism that preserves correctness.

## Lost Update

A lost update happens when two sessions read the same old value, both compute a
new value outside the database, and the later write overwrites the earlier
write. The Phase 6 ecommerce drill uses `ecommerce.inventory` as the hot row.

Reproduce it with two sessions:

```sql
-- session 1
BEGIN;
SELECT quantity_on_hand
FROM ecommerce.inventory
WHERE product_id = (
    SELECT id FROM ecommerce.products WHERE sku = 'BK-SQL-001'
);
```

```sql
-- session 2
BEGIN;
SELECT quantity_on_hand
FROM ecommerce.inventory
WHERE product_id = (
    SELECT id FROM ecommerce.products WHERE sku = 'BK-SQL-001'
);
```

If both sessions saw `1` and both write `0`, the system accepted two decisions
from one unit of inventory. Fix it with an atomic conditional update when the
counter row owns the whole invariant:

```sql
UPDATE ecommerce.inventory
SET quantity_on_hand = quantity_on_hand - 1
WHERE product_id = (
    SELECT id FROM ecommerce.products WHERE sku = 'BK-SQL-001'
)
  AND quantity_on_hand >= 1
RETURNING quantity_on_hand;
```

Fix it with `SELECT ... FOR UPDATE` when the read decision controls several
later statements in the same transaction:

```sql
BEGIN;
SELECT quantity_on_hand
FROM ecommerce.inventory
WHERE product_id = (
    SELECT id FROM ecommerce.products WHERE sku = 'BK-SQL-001'
)
FOR UPDATE;
-- insert reservation and update inventory while holding the row lock
COMMIT;
```

Use READ COMMITTED for the atomic update or explicit row lock pattern. Escalate
only if the invariant spans rows or predicates that the row lock does not cover.

## Write Skew

Write skew happens when two sessions read the same predicate, each updates a
different row, and the combined result violates an invariant that neither row
can enforce alone. The classic example is two clinicians on call: each sees
another clinician available, so each marks themself unavailable.

Under REPEATABLE READ, each transaction keeps a stable snapshot. That stable
snapshot can still be unsafe because the sessions update different rows. Neither
session directly conflicts with the other's row update, so both can commit.

The repair is usually one of these:

- Move the invariant into a constraint or schema design when the invariant can
  be represented that way.
- Lock a shared parent or guard row before making the decision.
- Use SERIALIZABLE and retry the whole transaction when PostgreSQL raises a
  serialization failure.

SERIALIZABLE is the right teaching tool for the write-skew drill because it
shows PostgreSQL rejecting a history that cannot be explained as one safe serial
order. Application code must treat SQLSTATE `40001` as retryable from the
transaction boundary.

## Phantom Reads and Range Checks

A phantom or range-check race appears when the application checks that no row
matches a predicate and then inserts a row that should have been protected by
that predicate. Appointment booking is the typical Phase 6 example:

```sql
BEGIN;
SELECT count(*)
FROM scheduling.appointment_holds
WHERE professional_id = 1
  AND hold_expires_at > now()
  AND slot && tstzrange(
      '2026-05-10 15:00:00+00',
      '2026-05-10 15:30:00+00',
      '[)'
  );
-- application sees zero and inserts
COMMIT;
```

Two sessions can both see zero before either insert commits. A row lock on the
missing row cannot help because the row does not exist yet. Practical fixes are:

- Add a schema-level exclusion constraint when the business rule is no overlap
  for active rows and the model can express it.
- Lock a coarser guard row, such as the professional row, before the range
  check and insert.
- Use SERIALIZABLE and retry serialization failures for predicate-shaped
  decisions.

For Phase 6, prefer the fix that is easiest to explain under concurrent load.
If the invariant is "one hold per professional per overlapping slot", a guard
row lock is understandable and portable. If the invariant is central and durable,
a constraint is stronger because it protects every writer, not only the current
application code path.
