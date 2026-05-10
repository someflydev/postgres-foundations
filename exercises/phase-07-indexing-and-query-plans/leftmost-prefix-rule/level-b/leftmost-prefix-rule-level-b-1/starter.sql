-- Capture estimated rows, actual rows, and buffers.
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE customer_id = 42
  AND placed_at >= '2025-01-01'::timestamptz
ORDER BY placed_at DESC
LIMIT 20;
