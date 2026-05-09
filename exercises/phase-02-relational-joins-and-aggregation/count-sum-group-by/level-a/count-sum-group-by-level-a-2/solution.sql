SELECT order_id, sum(quantity * unit_price) AS merchandise_total FROM ecommerce.order_items GROUP BY order_id ORDER BY order_id;
