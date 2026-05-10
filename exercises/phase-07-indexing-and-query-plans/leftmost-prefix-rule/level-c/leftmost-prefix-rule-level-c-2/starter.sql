-- Existing wrong-order index:
-- CREATE INDEX orders_placed_at_customer_wrong_phase7a_idx
-- ON ecommerce.orders (placed_at DESC, customer_id);
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE customer_id = 42
  AND placed_at >= '2025-01-01'::timestamptz
ORDER BY placed_at DESC
LIMIT 20;
