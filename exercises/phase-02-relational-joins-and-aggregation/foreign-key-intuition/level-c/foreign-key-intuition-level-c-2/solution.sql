SELECT p.sku, count(oi.id) AS item_rows FROM ecommerce.products p LEFT JOIN ecommerce.order_items oi ON oi.product_id = p.id GROUP BY p.sku ORDER BY p.sku;
