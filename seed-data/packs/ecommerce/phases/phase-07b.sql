-- domain: ecommerce
-- phase: 07b
-- depends: phase-07a
-- expected rows: uses phase 7a generated order volume
-- description: skewed order statuses and expression-index targets for advanced indexing labs

CREATE SCHEMA IF NOT EXISTS ecommerce;

UPDATE ecommerce.orders
SET status = CASE
    WHEN id % 100 < 92 THEN 'delivered'
    WHEN id % 100 < 96 THEN 'pending'
    WHEN id % 100 < 98 THEN 'refunded'
    ELSE 'canceled'
END,
updated_at = greatest(updated_at, placed_at)
WHERE status IN ('placed', 'paid', 'shipped', 'delivered', 'pending', 'refunded', 'canceled');

ANALYZE ecommerce.orders;
ANALYZE ecommerce.customers;
