ANALYZE ecommerce.orders;
EXPLAIN (ANALYZE, BUFFERS)
SELECT status, count(*)
FROM ecommerce.orders
WHERE placed_at >= '2025-01-01'::timestamptz
GROUP BY status;
