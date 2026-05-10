SELECT sku, name, brand,
       ts_rank_cd(product_search_vec, websearch_to_tsquery('english', 'postgres indexing')) AS rank
FROM ecommerce.products
WHERE product_search_vec @@ websearch_to_tsquery('english', 'postgres indexing')
ORDER BY rank DESC, name;
