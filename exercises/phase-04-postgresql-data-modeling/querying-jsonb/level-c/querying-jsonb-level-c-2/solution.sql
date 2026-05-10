SELECT order_number, jsonb_path_query(metadata, '$.fraud.score') AS fraud_score FROM ecommerce.orders ORDER BY order_number;
