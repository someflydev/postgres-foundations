SELECT id, title,
       ts_rank(search_vec, websearch_to_tsquery('english', 'postgres indexing')) AS rank
FROM documents.docs
WHERE search_vec @@ websearch_to_tsquery('english', 'postgres indexing')
ORDER BY rank DESC, published_at DESC
LIMIT 10;
