-- Baseline first, then add the lesson's candidate index and compare.
SELECT count(*)
FROM ecommerce.orders
WHERE status = 'paid';
