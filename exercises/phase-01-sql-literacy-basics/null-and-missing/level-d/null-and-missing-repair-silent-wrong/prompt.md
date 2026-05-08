# NULL and Missing Facts: Repair Silent Wrong

Seed pack: `ecommerce`, phase `1`.

Critique the broken query below. It returns rows without erroring, but it answers the wrong question. Repair it so the output matches the exercise title and success criteria.

```sql
SELECT * FROM ecommerce.customers ORDER BY 1 LIMIT 1;
```

Work against `ecommerce.customers` only. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `ecommerce` phase-1 seed pack.
- The returned rows and columns match the reference output by comparison.
- The answer uses only one table: `ecommerce.customers`.
- The answer ends with a semicolon.
