-- Run with pgfound lab explain and compare estimated rows, actual rows, and buffers.
EXPLAIN (ANALYZE, BUFFERS)
SELECT order_number, placed_at, total_amount
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC
LIMIT 20;
