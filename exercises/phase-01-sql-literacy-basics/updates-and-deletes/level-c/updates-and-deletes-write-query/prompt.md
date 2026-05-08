# UPDATE and DELETE Rows: Write Query

Seed pack: `scheduling`, phase `1`.

Write the UPDATE or DELETE independently against `scheduling.appointments` with a protective `WHERE` clause and `RETURNING`. Do not look at `solution.sql` until after you have made an attempt. The expected result is the same columns and rows as the success criteria describe for this exercise.

Work against `scheduling.appointments` only. Use `UPDATE` or `DELETE` with a `WHERE` clause and `RETURNING` so the changed row is visible. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `scheduling` phase-1 seed pack.
- The returned `RETURNING` rows and columns match the reference output by comparison.
- The answer uses only one table: `scheduling.appointments`.
- The answer ends with a semicolon.
