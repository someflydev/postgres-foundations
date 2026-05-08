# Shape of a Table: Recognize One

Seed pack: `ecommerce`, phase `1`.

Predict the rows returned by this one-table SQL before you run it:

```sql
SELECT sku, name FROM ecommerce.products ORDER BY sku;
```

Work against `ecommerce.products` only. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `ecommerce` phase-1 seed pack.
- The returned rows and columns match the reference output by comparison.
- The answer uses only one table: `ecommerce.products`.
- The answer ends with a semicolon.
