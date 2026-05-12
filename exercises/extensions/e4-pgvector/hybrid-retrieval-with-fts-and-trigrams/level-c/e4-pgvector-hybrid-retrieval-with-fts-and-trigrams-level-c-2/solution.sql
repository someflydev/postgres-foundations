WITH lexical AS (
    SELECT id, ts_rank(search_vec, websearch_to_tsquery('english', 'postgres indexing')) AS lexical_rank
    FROM documents.docs
    WHERE search_vec @@ websearch_to_tsquery('english', 'postgres indexing')
), vector_hits AS (
    SELECT id, 1.0 / (1.0 + (fake_embedding <=> documents.fake_embedding_text('postgres indexing')::vector)) AS vector_rank
    FROM documents.docs
    ORDER BY fake_embedding <=> documents.fake_embedding_text('postgres indexing')::vector
    LIMIT 100
)
SELECT d.id, d.title, coalesce(l.lexical_rank, 0) AS lexical_rank, coalesce(v.vector_rank, 0) AS vector_rank
FROM documents.docs AS d
LEFT JOIN lexical AS l ON l.id = d.id
LEFT JOIN vector_hits AS v ON v.id = d.id
WHERE l.id IS NOT NULL OR v.id IS NOT NULL
ORDER BY (coalesce(l.lexical_rank, 0) + coalesce(v.vector_rank, 0)) DESC, d.title
LIMIT 10;
