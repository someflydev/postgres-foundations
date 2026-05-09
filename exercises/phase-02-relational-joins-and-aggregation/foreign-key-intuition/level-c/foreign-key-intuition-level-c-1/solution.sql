SELECT o.order_number, count(oi.id) AS item_rows FROM ecommerce.orders o LEFT JOIN ecommerce.order_items oi ON oi.order_id = o.id GROUP BY o.order_number ORDER BY o.order_number;
