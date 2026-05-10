-- Expected reasoning:
-- Identify the scan node, table, estimated rows, actual rows, and whether the predicate is selective.
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*)
FROM ecommerce.orders
WHERE status = 'paid';
