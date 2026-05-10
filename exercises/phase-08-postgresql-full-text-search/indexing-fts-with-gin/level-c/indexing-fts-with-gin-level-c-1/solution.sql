EXPLAIN (ANALYZE, BUFFERS)
SELECT id, title
FROM documents.docs
WHERE body ILIKE '%postgres indexing%';

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, title
FROM documents.docs
WHERE search_vec @@ websearch_to_tsquery('english', 'postgres indexing');
