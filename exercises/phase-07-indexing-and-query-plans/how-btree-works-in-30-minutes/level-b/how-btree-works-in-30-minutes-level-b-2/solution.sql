-- Run with pgfound lab explain and compare estimated rows, actual rows, and buffers.
EXPLAIN (ANALYZE, BUFFERS)
SELECT status, count(*)
FROM ecommerce.orders
GROUP BY status
ORDER BY status;
