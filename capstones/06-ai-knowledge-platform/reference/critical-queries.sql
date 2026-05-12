SELECT document_id, title, ts_rank(search_tsv, plainto_tsquery('english', 'queue restart')) AS rank
FROM knowledge.documents
WHERE search_tsv @@ plainto_tsquery('english', 'queue restart')
ORDER BY rank DESC, updated_at DESC
LIMIT 10;

SELECT document_id, title, similarity(title, 'runbok') AS score
FROM knowledge.documents
WHERE title % 'runbok'
ORDER BY score DESC
LIMIT 10;

SELECT chunk_id, document_id
FROM knowledge.document_chunks
ORDER BY embedding <=> ('[' || repeat('0,', 1535) || '0]')::vector
LIMIT 10;

WITH lexical AS (
    SELECT document_id, row_number() OVER (ORDER BY ts_rank(search_tsv, plainto_tsquery('english', 'api authentication')) DESC) AS r
    FROM knowledge.documents
    WHERE search_tsv @@ plainto_tsquery('english', 'api authentication')
),
semantic AS (
    SELECT document_id, row_number() OVER (ORDER BY min(embedding <=> ('[' || repeat('0,', 1535) || '0]')::vector)) AS r
    FROM knowledge.document_chunks
    GROUP BY document_id
)
SELECT document_id, sum(1.0 / (60 + r)) AS rrf_score
FROM (
    SELECT * FROM lexical
    UNION ALL
    SELECT * FROM semantic
) ranked
GROUP BY document_id
ORDER BY rrf_score DESC
LIMIT 10;
