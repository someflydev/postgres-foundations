-- Preview only: pg_trgm is taught in depth in PROMPT_34.
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;
SELECT title
FROM documents.docs
WHERE title % 'postgress indexng'
ORDER BY similarity(title, 'postgress indexng') DESC
LIMIT 10;
