SELECT c.id, c.email, o.order_number FROM ecommerce.customers c INNER JOIN ecommerce.orders o ON o.customer_id = c.id ORDER BY c.id, o.order_number;
