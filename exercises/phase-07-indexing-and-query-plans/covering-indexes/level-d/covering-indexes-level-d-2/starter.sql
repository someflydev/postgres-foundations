-- Bad index under review:
-- CREATE INDEX orders_cover_everything_phase7a_idx
-- ON ecommerce.orders (customer_id, placed_at DESC)
-- INCLUDE (order_number, total_amount, status, currency, created_at, updated_at);
-- Diagnose whether this is justified for the hot projection.
SELECT order_number, placed_at, total_amount
FROM ecommerce.orders
WHERE customer_id = 42
ORDER BY placed_at DESC
LIMIT 20;
