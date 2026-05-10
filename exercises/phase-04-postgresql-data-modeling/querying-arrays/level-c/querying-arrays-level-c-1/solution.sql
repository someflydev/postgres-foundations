SELECT tag, count(*) FROM ecommerce.products CROSS JOIN unnest(tags) AS tag GROUP BY tag ORDER BY tag;
