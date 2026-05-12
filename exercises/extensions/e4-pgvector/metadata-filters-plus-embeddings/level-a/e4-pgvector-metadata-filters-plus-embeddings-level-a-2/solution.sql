SELECT id, title
FROM documents.docs
ORDER BY fake_embedding <=> documents.fake_embedding_text('restore planning')::vector
LIMIT 10;
