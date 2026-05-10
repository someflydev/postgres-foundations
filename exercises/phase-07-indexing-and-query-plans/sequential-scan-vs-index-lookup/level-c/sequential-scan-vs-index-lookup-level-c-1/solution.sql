DROP INDEX IF EXISTS ecommerce.orders_customer_recent_phase7a_idx;
CREATE INDEX orders_customer_recent_phase7a_idx ON ecommerce.orders (customer_id, placed_at DESC);
ANALYZE ecommerce.orders;

SELECT id, order_number, placed_at, total_amount
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC
LIMIT 1;
