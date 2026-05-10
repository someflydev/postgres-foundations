-- Broad predicate: explain why a sequential scan can be correct.
SELECT count(*)
FROM ecommerce.orders
WHERE status = 'paid';
