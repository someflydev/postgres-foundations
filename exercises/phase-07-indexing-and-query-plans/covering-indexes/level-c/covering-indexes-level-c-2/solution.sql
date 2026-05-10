DROP INDEX IF EXISTS ecommerce.orders_recent_covering_phase7a_idx;
CREATE INDEX orders_recent_covering_phase7a_idx ON ecommerce.orders (customer_id, placed_at DESC) INCLUDE (order_number, total_amount);
ANALYZE ecommerce.orders;

SELECT order_number, placed_at, total_amount
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC
LIMIT 20;
