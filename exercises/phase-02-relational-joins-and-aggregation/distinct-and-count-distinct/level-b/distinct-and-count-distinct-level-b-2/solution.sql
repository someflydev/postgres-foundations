SELECT p.sku, count(DISTINCT oi.order_id) AS orders_with_product FROM ecommerce.products p LEFT JOIN ecommerce.order_items oi ON oi.product_id = p.id GROUP BY p.sku ORDER BY p.sku;
