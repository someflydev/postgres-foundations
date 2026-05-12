SELECT id, title, ts_rank(search_vec, websearch_to_tsquery('english', 'postgres indexing')) AS lexical_rank
FROM documents.docs
WHERE search_vec @@ websearch_to_tsquery('english', 'postgres indexing')
ORDER BY lexical_rank DESC, title
LIMIT 10;
