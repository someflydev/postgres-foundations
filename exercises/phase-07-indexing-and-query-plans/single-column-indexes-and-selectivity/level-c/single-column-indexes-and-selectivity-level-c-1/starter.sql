-- Baseline first, then add the lesson's candidate index and compare.
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC;
