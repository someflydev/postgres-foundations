# Solution

The missing invariant is not just the final constraint; it is the migration order that makes the constraint safe to add. Without this constraint, an incident could occur when old NULL totals survive and a new invoice report treats missing money as a valid amount.

A concrete repair is:

```sql
SELECT count(*) FROM ecommerce.orders WHERE total_amount IS NULL OR total_amount < 0;

UPDATE ecommerce.orders
SET total_amount = 0
WHERE total_amount IS NULL;

ALTER TABLE ecommerce.orders
    ALTER COLUMN total_amount SET DEFAULT 0,
    ALTER COLUMN total_amount SET NOT NULL;

ALTER TABLE ecommerce.orders
    ADD CONSTRAINT orders_total_amount_nonnegative CHECK (total_amount >= 0);
```

The order is inspect, clean, backfill, enforce, and verify. PostgreSQL rejecting the ALTER TABLE is a useful signal that hidden data debt remains.
