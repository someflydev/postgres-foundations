-- Expected reasoning:
-- This broad status predicate usually favors a sequential scan because it keeps many rows.
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*)
FROM ecommerce.orders
WHERE status = 'paid';
