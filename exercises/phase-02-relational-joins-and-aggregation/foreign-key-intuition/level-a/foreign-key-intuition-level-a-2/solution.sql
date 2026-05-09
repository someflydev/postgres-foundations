SELECT o.order_number, c.email FROM ecommerce.orders o INNER JOIN ecommerce.customers c ON c.id = o.customer_id ORDER BY o.order_number;
