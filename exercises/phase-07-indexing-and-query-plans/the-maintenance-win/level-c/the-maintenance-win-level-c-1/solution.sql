CREATE INDEX IF NOT EXISTS orders_open_status_partial_idx
ON ecommerce.orders (placed_at DESC)
WHERE status IN ('pending', 'refunded', 'canceled');
ANALYZE ecommerce.orders;
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, status, placed_at
FROM ecommerce.orders
WHERE status IN ('pending', 'refunded', 'canceled')
ORDER BY placed_at DESC
LIMIT 100;
