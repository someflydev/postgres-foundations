SELECT
    customer_id,
    order_number,
    placed_at::date AS ordered_on,
    total_amount,
    sum(total_amount) OVER (
        PARTITION BY customer_id
        ORDER BY placed_at, id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_customer_revenue,
    dense_rank() OVER (PARTITION BY customer_id ORDER BY total_amount DESC) AS revenue_rank
FROM ecommerce.orders
ORDER BY customer_id, placed_at, id
LIMIT 30;
