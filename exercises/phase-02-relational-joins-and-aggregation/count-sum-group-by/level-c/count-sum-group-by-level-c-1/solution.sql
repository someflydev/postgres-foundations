SELECT order_id, count(*) AS item_rows FROM ecommerce.order_items GROUP BY order_id HAVING count(*) >= 2 ORDER BY order_id;
