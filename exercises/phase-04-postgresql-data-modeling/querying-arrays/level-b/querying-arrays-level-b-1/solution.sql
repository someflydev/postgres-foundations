SELECT sku FROM ecommerce.products WHERE 'gift' = ANY (tags) ORDER BY sku;
