SELECT array_agg(sku ORDER BY sku) FROM ecommerce.products WHERE tags @> ARRAY['postgres']::text[];
