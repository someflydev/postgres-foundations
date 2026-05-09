SELECT oi.id, o.order_number, oi.quantity FROM ecommerce.order_items oi INNER JOIN ecommerce.orders o ON o.id = oi.order_id ORDER BY oi.id;
