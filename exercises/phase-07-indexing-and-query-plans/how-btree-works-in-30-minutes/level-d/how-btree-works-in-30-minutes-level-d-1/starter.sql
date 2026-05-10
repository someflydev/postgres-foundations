-- Bad index under review:
-- CREATE INDEX orders_status_phase7a_idx ON ecommerce.orders (status);
-- The hot query is broad and the write path maintains one more B-tree.
SELECT count(*)
FROM ecommerce.orders
WHERE status = 'paid';
