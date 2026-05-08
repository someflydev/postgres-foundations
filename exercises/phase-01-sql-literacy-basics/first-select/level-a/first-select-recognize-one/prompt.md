# First SELECT: Recognize One

Seed pack: `scheduling`, phase `1`.

Predict the rows returned by this one-table SQL before you run it:

```sql
SELECT display_name, specialty FROM scheduling.providers ORDER BY display_name;
```

Work against `scheduling.providers` only. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `scheduling` phase-1 seed pack.
- The returned rows and columns match the reference output by comparison.
- The answer uses only one table: `scheduling.providers`.
- The answer ends with a semicolon.
