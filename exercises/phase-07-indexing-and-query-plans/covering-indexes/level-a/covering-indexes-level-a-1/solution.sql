-- Expected reasoning:
-- Identify the scan node, table, estimated rows, actual rows, and whether the predicate is selective.
EXPLAIN (ANALYZE, BUFFERS)
SELECT order_number, placed_at, total_amount
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC
LIMIT 20;
