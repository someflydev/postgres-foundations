# INSERT Rows: Complete Order

Seed pack: `ecommerce`, phase `1`.

Write a one-table INSERT against `ecommerce.products` with an explicit column list. Use the scaffold in `starter.sql` if present. Your output must match the intended row set for `INSERT Rows: Complete Order`.

Work against `ecommerce.products` only. Use `INSERT` with an explicit column list and `RETURNING` so the changed row is visible. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `ecommerce` phase-1 seed pack.
- The returned `RETURNING` rows and columns match the reference output by comparison.
- The answer uses only one table: `ecommerce.products`.
- The answer ends with a semicolon.
