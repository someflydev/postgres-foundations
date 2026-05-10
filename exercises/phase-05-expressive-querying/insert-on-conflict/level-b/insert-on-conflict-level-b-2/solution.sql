INSERT INTO ecommerce.product_daily_inventory (sku, snapshot_date, quantity_on_hand)
VALUES ('BK-SQL-001', DATE '2026-05-01', 31)
ON CONFLICT (sku, snapshot_date) DO UPDATE
SET quantity_on_hand = EXCLUDED.quantity_on_hand,
    updated_at = now()
RETURNING sku, snapshot_date, quantity_on_hand;
