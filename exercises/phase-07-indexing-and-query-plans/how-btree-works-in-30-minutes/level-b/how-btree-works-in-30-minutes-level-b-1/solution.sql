-- Run with pgfound lab explain and compare estimated rows, actual rows, and buffers.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE placed_at >= '2025-12-01'::timestamptz
ORDER BY placed_at DESC
LIMIT 20;
