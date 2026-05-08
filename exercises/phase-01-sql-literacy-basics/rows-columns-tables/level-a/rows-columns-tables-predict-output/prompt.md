# Rows, Columns, Tables: Predict Output

Seed pack: `ecommerce`, phase `1`.

Predict the rows returned by this one-table SQL before you run it:

```sql
SELECT sku, price FROM ecommerce.products WHERE price BETWEEN 10 AND 30 ORDER BY price;
```

Work against `ecommerce.products` only. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `ecommerce` phase-1 seed pack.
- The returned rows and columns match the reference output by comparison.
- The answer uses only one table: `ecommerce.products`.
- The answer ends with a semicolon.
