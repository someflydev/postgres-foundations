SELECT order_number, pg_typeof(metadata)::text AS metadata_type FROM ecommerce.orders ORDER BY order_number;
