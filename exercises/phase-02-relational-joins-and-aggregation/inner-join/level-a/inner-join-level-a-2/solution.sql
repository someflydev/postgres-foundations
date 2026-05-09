SELECT oi.id, p.sku FROM ecommerce.order_items oi INNER JOIN ecommerce.products p ON p.id = oi.product_id ORDER BY oi.id;
