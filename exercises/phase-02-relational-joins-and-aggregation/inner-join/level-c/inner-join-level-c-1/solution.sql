SELECT c.email, o.order_number FROM ecommerce.customers c INNER JOIN ecommerce.orders o ON o.customer_id = c.id ORDER BY c.email, o.order_number;
