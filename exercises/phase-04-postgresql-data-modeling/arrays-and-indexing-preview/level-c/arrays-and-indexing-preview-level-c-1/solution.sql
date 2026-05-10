SELECT sku FROM ecommerce.products WHERE 'training' = ANY (tags) ORDER BY sku;
