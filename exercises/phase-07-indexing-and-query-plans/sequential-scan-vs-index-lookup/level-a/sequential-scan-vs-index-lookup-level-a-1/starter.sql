-- Predict the access path, then run with pgfound lab explain.
SELECT id, order_number, placed_at, total_amount
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC
LIMIT 1;
