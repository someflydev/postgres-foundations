CREATE SCHEMA IF NOT EXISTS knowledge;

CREATE TABLE knowledge.documents (
    document_id bigserial PRIMARY KEY,
    title text NOT NULL,
    body text NOT NULL
);
