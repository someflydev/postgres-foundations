SELECT order_number, pg_typeof(ordered_at)::text AS stored_type FROM ecommerce.orders ORDER BY order_number;
