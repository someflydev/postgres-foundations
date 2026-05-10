DROP INDEX IF EXISTS ecommerce.orders_status_phase7a_idx;
CREATE INDEX orders_status_phase7a_idx ON ecommerce.orders (status);
ANALYZE ecommerce.orders;

SELECT count(*)
FROM ecommerce.orders
WHERE status = 'paid';
