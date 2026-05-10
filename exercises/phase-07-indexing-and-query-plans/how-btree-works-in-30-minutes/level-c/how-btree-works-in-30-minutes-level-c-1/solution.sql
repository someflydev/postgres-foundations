DROP INDEX IF EXISTS ecommerce.orders_placed_at_phase7a_idx;
CREATE INDEX orders_placed_at_phase7a_idx ON ecommerce.orders (placed_at DESC NULLS LAST);
ANALYZE ecommerce.orders;

SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE placed_at >= '2025-12-01'::timestamptz
ORDER BY placed_at DESC
LIMIT 20;
