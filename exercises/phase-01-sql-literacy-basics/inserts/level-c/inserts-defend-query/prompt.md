# INSERT Rows: Defend Query

Seed pack: `ecommerce`, phase `1`.

Write the INSERT independently against `ecommerce.products` with an explicit column list and `RETURNING`. Do not look at `solution.sql` until after you have made an attempt. The expected result is the same columns and rows as the success criteria describe for this exercise.

Work against `ecommerce.products` only. Use `INSERT` with an explicit column list and `RETURNING` so the changed row is visible. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `ecommerce` phase-1 seed pack.
- The returned `RETURNING` rows and columns match the reference output by comparison.
- The answer uses only one table: `ecommerce.products`.
- The answer ends with a semicolon.
