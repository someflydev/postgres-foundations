# NULL and Missing Facts: Recognize One

Seed pack: `ecommerce`, phase `1`.

Predict the rows returned by this one-table SQL before you run it:

```sql
SELECT email, full_name FROM ecommerce.customers ORDER BY email;
```

Work against `ecommerce.customers` only. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `ecommerce` phase-1 seed pack.
- The returned rows and columns match the reference output by comparison.
- The answer uses only one table: `ecommerce.customers`.
- The answer ends with a semicolon.
