SELECT count(*) FROM ecommerce.products WHERE tags @> ARRAY['postgres']::text[];
