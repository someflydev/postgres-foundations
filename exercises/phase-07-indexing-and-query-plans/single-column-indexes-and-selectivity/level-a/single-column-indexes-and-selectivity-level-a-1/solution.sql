-- Expected reasoning:
-- Identify the scan node, table, estimated rows, actual rows, and whether the predicate is selective.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC;
