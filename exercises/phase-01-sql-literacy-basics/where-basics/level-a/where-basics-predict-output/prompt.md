# WHERE Basics: Predict Output

Seed pack: `ecommerce`, phase `1`.

Predict the rows returned by this one-table SQL before you run it:

```sql
SELECT order_number, total_amount FROM ecommerce.orders WHERE status IN ('paid', 'placed') ORDER BY total_amount;
```

Work against `ecommerce.orders` only. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `ecommerce` phase-1 seed pack.
- The returned rows and columns match the reference output by comparison.
- The answer uses only one table: `ecommerce.orders`.
- The answer ends with a semicolon.
