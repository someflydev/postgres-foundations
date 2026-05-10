WITH paid_orders AS NOT MATERIALIZED (
    SELECT customer_id, total_amount, placed_at
    FROM ecommerce.orders
    WHERE status IN ('paid', 'shipped', 'delivered')
)
SELECT customer_id, count(*) AS paid_orders, sum(total_amount) AS revenue
FROM paid_orders
GROUP BY customer_id
ORDER BY revenue DESC, customer_id
LIMIT 10;
