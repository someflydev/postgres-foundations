SELECT
    customer_id,
    order_number,
    placed_at::date AS ordered_on,
    total_amount,
    count(*) OVER (PARTITION BY customer_id) AS customer_order_count
FROM ecommerce.orders
ORDER BY customer_id, placed_at, order_number
LIMIT 20;
