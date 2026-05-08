# INSERT Rows: Recognize One

Seed pack: `ecommerce`, phase `1`.

Predict the row or rows returned by this one-table INSERT ... RETURNING statement before you run it:

```sql
INSERT INTO ecommerce.products (sku, name, price, stock_on_hand) VALUES ('CARD-PG-001', 'Postgres Sticker Pack', 5.00, 100) RETURNING sku, name, price;
```

Work against `ecommerce.products` only. Use `INSERT` with an explicit column list and `RETURNING` so the changed row is visible. Do not use joins, grouping, aggregates, CTEs, window functions, transactions, indexes, subqueries, function definitions, JSON, or arrays.

Success criteria:

- The statement runs cleanly against the `ecommerce` phase-1 seed pack.
- The returned `RETURNING` rows and columns match the reference output by comparison.
- The answer uses only one table: `ecommerce.products`.
- The answer ends with a semicolon.
