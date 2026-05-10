WITH monthly_orders AS (
    SELECT date_trunc('month', placed_at)::date AS month_start, customer_id, sum(total_amount) AS revenue
    FROM ecommerce.orders
    GROUP BY 1, 2
), customer_months AS (
    SELECT month_start, count(*) AS active_customers, sum(revenue) AS revenue
    FROM monthly_orders
    GROUP BY month_start
)
SELECT month_start, active_customers, revenue
FROM customer_months
ORDER BY month_start;
