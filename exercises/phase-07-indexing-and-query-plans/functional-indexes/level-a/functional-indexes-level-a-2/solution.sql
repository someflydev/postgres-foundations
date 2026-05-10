CREATE INDEX IF NOT EXISTS orders_placed_day_idx
ON ecommerce.orders ((date_trunc('day', placed_at)));
ANALYZE ecommerce.orders;
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*)
FROM ecommerce.orders
WHERE date_trunc('day', placed_at) = '2025-03-01'::date;
