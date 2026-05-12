CREATE INDEX IF NOT EXISTS documents_search_tsv_gin
    ON knowledge.documents USING gin (search_tsv);
CREATE INDEX IF NOT EXISTS documents_title_trgm_gin
    ON knowledge.documents USING gin (title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS document_chunks_embedding_hnsw
    ON knowledge.document_chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS document_chunks_document_idx
    ON knowledge.document_chunks (document_id, chunk_ordinal);
