SELECT title, similarity(title, 'postgress indexing') AS score
FROM documents.docs
WHERE title % 'postgress indexing'
ORDER BY score DESC, title
LIMIT 10;
