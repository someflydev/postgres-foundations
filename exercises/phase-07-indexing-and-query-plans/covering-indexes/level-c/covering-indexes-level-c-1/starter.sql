-- Baseline first, then add the lesson's candidate index and compare.
SELECT order_number, placed_at, total_amount
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC
LIMIT 20;
