# UPDATE and DELETE Rows: Complete Order

Seed pack: `scheduling`, phase `1`.

Write a one-table UPDATE or DELETE against `scheduling.appointments` with a protective `WHERE` clause. Use the scaffold in `starter.sql` if present. Your output must match the intended row set for `UPDATE and DELETE Rows: Complete Order`.

Work against `scheduling.appointments` only. Use `UPDATE` or `DELETE` with a `WHERE` clause and `RETURNING` so the changed row is visible. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `scheduling` phase-1 seed pack.
- The returned `RETURNING` rows and columns match the reference output by comparison.
- The answer uses only one table: `scheduling.appointments`.
- The answer ends with a semicolon.
