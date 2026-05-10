-- Capture estimated rows, actual rows, and buffers.
SELECT count(*)
FROM ecommerce.orders
WHERE status = 'paid';
