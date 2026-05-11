SELECT c1.customer_id AS left_customer_id,
       c2.customer_id AS right_customer_id,
       word_similarity(c1.full_name, c2.full_name) AS name_score
FROM ecommerce.customers AS c1
JOIN ecommerce.customers AS c2 ON c1.customer_id < c2.customer_id
WHERE word_similarity(c1.full_name, c2.full_name) >= 0.72
ORDER BY name_score DESC, left_customer_id, right_customer_id;
