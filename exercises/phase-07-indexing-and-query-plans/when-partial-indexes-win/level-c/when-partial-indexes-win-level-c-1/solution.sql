DROP INDEX IF EXISTS ecommerce.orders_status_full_idx;
DROP INDEX IF EXISTS ecommerce.orders_pending_recent_idx;
CREATE INDEX orders_status_full_idx ON ecommerce.orders (status);
ANALYZE ecommerce.orders;
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE status = 'pending'
ORDER BY placed_at DESC
LIMIT 50;
DROP INDEX ecommerce.orders_status_full_idx;
CREATE INDEX orders_pending_recent_idx
ON ecommerce.orders (placed_at DESC)
WHERE status = 'pending';
ANALYZE ecommerce.orders;
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, placed_at
FROM ecommerce.orders
WHERE status = 'pending'
ORDER BY placed_at DESC
LIMIT 50;
