SELECT c.email, count(o.id) AS order_count FROM ecommerce.customers c LEFT JOIN ecommerce.orders o ON o.customer_id = c.id GROUP BY c.email ORDER BY c.email;
