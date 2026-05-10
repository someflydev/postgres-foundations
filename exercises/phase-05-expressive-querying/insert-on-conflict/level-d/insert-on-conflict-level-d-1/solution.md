# Solution

`ON CONFLICT DO NOTHING` is correct only when duplicate input means "we already
have the fact and there is nothing to change." Inventory snapshots do not have
that meaning here. The business requirement is "for this SKU and date, keep the
latest known quantity." Silently doing nothing preserves stale
`quantity_on_hand` values and makes the report look current when it is not.

The repair is an upsert that updates the mutable columns from `EXCLUDED`:

```sql
INSERT INTO ecommerce.product_daily_inventory (sku, snapshot_date, quantity_on_hand)
VALUES ('BK-SQL-001', DATE '2026-05-01', 31)
ON CONFLICT (sku, snapshot_date) DO UPDATE
SET quantity_on_hand = EXCLUDED.quantity_on_hand,
    updated_at = now()
RETURNING sku, snapshot_date, quantity_on_hand;
```

The defense should distinguish identity from state. The key
`(sku, snapshot_date)` identifies the snapshot row. The quantity is state that
can legitimately change as a new feed arrives, so `DO UPDATE` matches the
contract and `DO NOTHING` does not.
