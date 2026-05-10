-- Run with pgfound lab explain and compare estimated rows, actual rows, and buffers.
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*)
FROM ecommerce.orders
WHERE status = 'paid';
