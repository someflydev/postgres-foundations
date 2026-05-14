# Phase 6 Lessons

Phase 6 moves from single-session correctness to overlapping work. Learners
observe transactions, MVCC, isolation, lock behavior, races, deadlocks, and
retry-safe operations in PostgreSQL instead of treating concurrency as timing
luck.

| Cluster | Lesson | Title |
| --- | --- | --- |
| transactions | what-a-transaction-is | What a Transaction Is |
| transactions | begin-commit-rollback-and-error-handling | BEGIN, COMMIT, ROLLBACK, and Error Handling |
| mvcc | mvcc-in-30-minutes | MVCC in 30 Minutes |
| isolation | read-committed-is-the-default | READ COMMITTED Is the Default |
| isolation | repeatable-read-and-snapshot-isolation | REPEATABLE READ and Snapshot Isolation |
| isolation | serializable-and-predicate-locking | SERIALIZABLE and Predicate Locking |
| races | lost-update | Lost Update |
| races | write-skew | Write Skew |
| races | phantom-reads-and-range-checks | Phantom Reads and Range Checks |
| locks | select-for-update-vs-for-no-key-update | SELECT FOR UPDATE vs FOR NO KEY UPDATE |
| deadlocks | why-deadlocks-happen-and-how-to-avoid-them | Why Deadlocks Happen and How to Avoid Them |
| idempotency | making-operations-safe-to-retry | Making Operations Safe to Retry |
