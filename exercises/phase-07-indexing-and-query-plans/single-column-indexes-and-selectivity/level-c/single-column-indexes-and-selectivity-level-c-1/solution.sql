DROP INDEX IF EXISTS ecommerce.orders_customer_id_phase7a_idx;
CREATE INDEX orders_customer_id_phase7a_idx ON ecommerce.orders (customer_id);
ANALYZE ecommerce.orders;

SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC;
