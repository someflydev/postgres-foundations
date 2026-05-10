# BEGIN, COMMIT, ROLLBACK, and Error Handling

## Problem Framing

Correctness under concurrent access is the part of PostgreSQL that turns SQL from a reporting language into a system of record. A single session can make many examples look correct, but production work is almost never single-session work. Web requests overlap, jobs retry, dashboards read while workers write, and operators run repair scripts during incidents. The practical question is not whether one statement is syntactically valid. The question is whether a business invariant still holds when two sessions touch nearby facts at the same time.

In this lesson, the concrete incident is that a batch checkout script hits one bad row and then every later statement reports that the transaction is aborted. The initial symptom is usually not a dramatic database outage. It is an order count that does not match inventory, an appointment that exists twice, a payment job that cannot be safely retried, or a worker that waits long enough for the application to time out. PostgreSQL gives you transactions, MVCC, isolation levels, row locks, predicate protection, deadlock detection, savepoints, and durable uniqueness tools. Those tools are useful only when the developer can connect them to the invariant being protected.

The doctrine for this phase is intentionally direct: correctness is not an advanced topic saved for after performance. Correctness is the point. Indexes can make a wrong transaction faster. Clever query forms can make a broken invariant harder to notice. Extensions can add capability, but they do not remove the need to reason about concurrent reads and writes. The default recommendation is to use PostgreSQL core behavior first, understand exactly what it guarantees, and strengthen the mechanism only when the workload demands it.

## Minimal Concept Introduction

This lesson focuses on `begin_commit_rollback`, `transaction`. Treat these terms as operational tools. A transaction gives a boundary around work. ACID names the promise that the boundary is atomic, consistent with database rules, isolated from incompatible concurrent work, and durable after commit. MVCC lets a reader see a snapshot while writers create newer row versions. READ COMMITTED gives each statement a fresh snapshot. REPEATABLE READ gives the transaction a stable snapshot. SERIALIZABLE asks PostgreSQL to reject dangerous interleavings so the committed result matches some serial order.

Locks are not a punishment; they are how sessions coordinate around shared facts. `SELECT ... FOR UPDATE` says that the row you read is the row you intend to change or protect from change. `SELECT ... FOR NO KEY UPDATE` is weaker and often sufficient when the key relationship should not be blocked. Predicate protection matters when the invariant is about absence, such as no overlapping booking. Deadlocks happen when sessions acquire locks in inconsistent order. PostgreSQL detects the cycle and aborts one transaction, so application code must be able to retry the whole unit of work.

The most important habit is to state the invariant before choosing syntax. If the invariant is inventory cannot go below zero, a single atomic update with a predicate may be enough. If the invariant is exactly one active hold for a slot, a constraint or exclusion rule may be better than a hand-written check. If the invariant spans several rows that might not exist yet, SERIALIZABLE or a schema-level constraint is often more honest than a loose check-then-insert pattern.

## Worked Example

Imagine an ecommerce flash sale at 3 AM on Sunday. Product `BK-SQL-001` has one unit left in `ecommerce.inventory`. Two workers both read the row, both see quantity one, both decide the sale is allowed, and both write quantity zero after inserting reservations. Each worker can truthfully say its local transaction looked reasonable. Together they oversold.

The naive shape is easy to recognize:

```sql
BEGIN;
SELECT quantity_on_hand FROM ecommerce.inventory WHERE product_id = 1;
-- application decides quantity_on_hand >= 1
UPDATE ecommerce.inventory SET quantity_on_hand = 0 WHERE product_id = 1;
COMMIT;
```

The repair is not to hope the application is fast. One repair is an atomic conditional update:

```sql
UPDATE ecommerce.inventory
SET quantity_on_hand = quantity_on_hand - 1
WHERE product_id = 1
  AND quantity_on_hand >= 1
RETURNING quantity_on_hand;
```

If the update returns no row, the reservation did not happen. Another repair is to lock the row before deciding:

```sql
BEGIN;
SELECT quantity_on_hand
FROM ecommerce.inventory
WHERE product_id = 1
FOR UPDATE;
-- decide while holding the row lock
UPDATE ecommerce.inventory
SET quantity_on_hand = quantity_on_hand - 1
WHERE product_id = 1;
COMMIT;
```

Those two repairs have different operational costs. The atomic update is compact and avoids a separate read decision. The explicit lock is clearer when several related writes follow the decision. In either case, the application must handle waiting, timeouts, and retryable failures. The database is doing useful coordination, but it is not a substitute for a clear unit of work.

## Diagnostic Questions

Ask four questions whenever a concurrent workflow looks suspicious. What invariant must remain true after both sessions commit? Which statement reads the fact that drives the decision? Which statement changes the fact or creates a conflicting fact? What happens if the two sessions swap order at the most inconvenient point?

For BEGIN, COMMIT, ROLLBACK, and Error Handling, the diagnostic lens is concrete. If the invariant is row-local, protect the row or use one atomic statement. If the invariant is range-shaped, protect the searched range or make the schema reject overlap. If failure is expected under SERIALIZABLE, treat `40001` as a signal to retry the whole transaction, not as proof that PostgreSQL is unreliable. If a deadlock appears, inspect the ordering of locks before increasing timeouts.

## Common Pitfalls

The first pitfall is confusing a transaction with a lock. `BEGIN` does not freeze the world. It only creates a boundary for commit and rollback. The second pitfall is assuming REPEATABLE READ means every invariant is safe. It gives a stable snapshot, but write skew can still happen when two sessions update different rows after reading the same predicate. The third pitfall is making retry logic unsafe. Retrying a payment, order reservation, or appointment hold without an idempotency key can duplicate the work you meant to protect.

Another common mistake is choosing the strongest mechanism without explaining the workload. SERIALIZABLE is valuable, but it brings retry behavior. Explicit locks are clear, but they can block. Advisory locks can coordinate application concepts, but they are easy to misuse because PostgreSQL cannot infer the protected rows. The right answer is the least surprising mechanism that preserves the invariant under the expected concurrent operations.

## Explain It Back

A good explanation names the sessions separately. Session 1 reads this row or predicate. Session 2 reads the same row or predicate. Session 1 writes this fact. Session 2 writes that fact. Under READ COMMITTED, each statement sees a current committed snapshot, so a later statement may see more than an earlier one. Under REPEATABLE READ, both decisions may be based on a stable but incomplete snapshot. Under SERIALIZABLE, PostgreSQL may abort one transaction because the combined history cannot be made serial.

The mitigation should be equally specific. Use `FOR UPDATE` when the read row is about to drive a write. Use `FOR NO KEY UPDATE` when you need to protect row content but do not need to block key changes. Use an atomic conditional update when a single row contains the whole counter invariant. Use constraints, exclusion rules, or SERIALIZABLE for absence and range invariants. Use savepoints for recoverable sub-steps inside a transaction, and use idempotency keys for operations that the client might retry after a timeout.

## References and Further Reading

- `docs/concurrency-playbook.md` summarizes lost update, write skew, and phantom or range-check races.
- `docs/glossary.md` defines the Phase 6 vocabulary used in this lesson.
- PostgreSQL documentation sections on transactions, MVCC, explicit locking, and transaction isolation are the canonical references for exact behavior.
