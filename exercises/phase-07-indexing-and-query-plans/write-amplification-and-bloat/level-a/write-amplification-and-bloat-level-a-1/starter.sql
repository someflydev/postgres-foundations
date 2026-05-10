-- Predict the access path, then run with pgfound lab explain.
SELECT count(*)
FROM ecommerce.orders
WHERE status = 'paid';
