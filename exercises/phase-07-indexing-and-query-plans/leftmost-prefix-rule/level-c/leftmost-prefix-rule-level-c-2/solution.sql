DROP INDEX IF EXISTS ecommerce.orders_customer_placed_at_phase7a_idx;
CREATE INDEX orders_customer_placed_at_phase7a_idx ON ecommerce.orders (customer_id, placed_at DESC);
ANALYZE ecommerce.orders;

SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE customer_id = 42
  AND placed_at >= '2025-01-01'::timestamptz
ORDER BY placed_at DESC
LIMIT 20;
