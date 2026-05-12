CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS knowledge;

CREATE TABLE knowledge.documents (
    document_id bigserial PRIMARY KEY,
    source_system text NOT NULL,
    title text NOT NULL,
    body text NOT NULL,
    team_slug text NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now(),
    search_tsv tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', title), 'A') ||
        setweight(to_tsvector('english', body), 'B')
    ) STORED
);

CREATE TABLE knowledge.document_chunks (
    chunk_id bigserial PRIMARY KEY,
    document_id bigint NOT NULL REFERENCES knowledge.documents(document_id) ON DELETE CASCADE,
    chunk_ordinal integer NOT NULL,
    chunk_text text NOT NULL,
    embedding_model text NOT NULL,
    embedding vector(1536) NOT NULL,
    UNIQUE (document_id, chunk_ordinal, embedding_model)
);
