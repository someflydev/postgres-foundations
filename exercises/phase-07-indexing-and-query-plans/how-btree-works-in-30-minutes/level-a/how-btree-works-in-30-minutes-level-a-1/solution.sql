-- Expected reasoning:
-- Identify the scan node, table, estimated rows, actual rows, and whether the predicate is selective.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE placed_at >= '2025-12-01'::timestamptz
ORDER BY placed_at DESC
LIMIT 20;
