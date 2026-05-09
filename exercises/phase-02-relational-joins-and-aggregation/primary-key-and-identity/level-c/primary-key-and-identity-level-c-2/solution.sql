SELECT c.id, c.email, o.id AS order_id FROM ecommerce.customers c LEFT JOIN ecommerce.orders o ON o.customer_id = c.id ORDER BY c.id, o.id;
