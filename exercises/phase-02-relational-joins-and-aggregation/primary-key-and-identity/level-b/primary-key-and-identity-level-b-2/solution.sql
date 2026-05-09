SELECT customer_id, count(*) AS order_count FROM ecommerce.orders GROUP BY customer_id ORDER BY customer_id;
