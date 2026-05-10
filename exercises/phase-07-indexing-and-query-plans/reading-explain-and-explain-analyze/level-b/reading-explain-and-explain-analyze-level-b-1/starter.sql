-- Capture estimated rows, actual rows, and buffers.
SELECT id, order_number, placed_at, total_amount
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC
LIMIT 1;
