# UPDATE and DELETE Rows: Predict Output

Seed pack: `scheduling`, phase `1`.

Predict the row or rows returned by this one-table UPDATE/DELETE ... RETURNING statement before you run it:

```sql
DELETE FROM scheduling.appointments WHERE starts_at = '2026-02-12 19:00:00+00' RETURNING starts_at, status;
```

Work against `scheduling.appointments` only. Use `UPDATE` or `DELETE` with a `WHERE` clause and `RETURNING` so the changed row is visible. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `scheduling` phase-1 seed pack.
- The returned `RETURNING` rows and columns match the reference output by comparison.
- The answer uses only one table: `scheduling.appointments`.
- The answer ends with a semicolon.
