SELECT order_number FROM ecommerce.orders WHERE metadata @> '{"gift": true}'::jsonb ORDER BY order_number;
