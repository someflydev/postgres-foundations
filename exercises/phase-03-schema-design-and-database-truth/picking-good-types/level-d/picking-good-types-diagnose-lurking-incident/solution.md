# Solution

The missing invariant is that money-like values, instants, and boolean facts need PostgreSQL types that preserve their meaning. Without this constraint, an incident could occur when a float rounding artifact changes a billed total or a timestamp without time zone is interpreted differently by two services.

A concrete repair is:

```sql
ALTER TABLE ecommerce.orders
    ALTER COLUMN total_amount TYPE numeric(12,2),
    ALTER COLUMN placed_at TYPE timestamptz,
    ALTER COLUMN total_amount SET NOT NULL;

ALTER TABLE ecommerce.orders
    ADD CONSTRAINT orders_total_amount_nonnegative CHECK (total_amount >= 0);
```

Prefer `text` over arbitrary `varchar(n)` unless the limit is a real rule, `numeric` over `float` for exact money, `timestamptz` for instants, and `boolean` for true yes-or-no facts.
