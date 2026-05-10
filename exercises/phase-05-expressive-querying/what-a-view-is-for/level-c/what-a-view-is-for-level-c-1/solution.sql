CREATE OR REPLACE VIEW ecommerce.customer_order_summary AS
SELECT c.id AS customer_id, c.email, count(o.id) AS order_count, coalesce(sum(o.total_amount), 0) AS lifetime_revenue
FROM ecommerce.customers c
LEFT JOIN ecommerce.orders o ON o.customer_id = c.id
GROUP BY c.id, c.email;

SELECT email, order_count, lifetime_revenue
FROM ecommerce.customer_order_summary
ORDER BY lifetime_revenue DESC, email
LIMIT 20;
