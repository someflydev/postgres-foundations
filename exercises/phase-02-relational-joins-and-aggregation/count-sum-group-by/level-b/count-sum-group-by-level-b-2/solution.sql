SELECT order_id, count(*) AS item_rows, sum(quantity * unit_price) AS merchandise_total FROM ecommerce.order_items GROUP BY order_id ORDER BY order_id;
