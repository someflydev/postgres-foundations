-- domain: document_search
-- phase: 02
-- depends: phase-01
-- description: tags and bridge rows for many-to-many joins

CREATE SCHEMA IF NOT EXISTS documents;

CREATE TABLE IF NOT EXISTS documents.tags (
    id bigint generated always as identity PRIMARY KEY,
    slug text NOT NULL UNIQUE,
    label text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS documents.document_tags (
    id bigint generated always as identity PRIMARY KEY,
    document_id bigint NOT NULL REFERENCES documents.documents(id),
    tag_id bigint NOT NULL REFERENCES documents.tags(id),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (document_id, tag_id)
);

INSERT INTO documents.tags (slug, label)
VALUES
    ('operations', 'Operations'),
    ('performance', 'Performance')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO documents.document_tags (document_id, tag_id)
VALUES
    (
        (SELECT id FROM documents.documents WHERE slug = 'backup-checklist'),
        (SELECT id FROM documents.tags WHERE slug = 'operations')
    ),
    (
        (SELECT id FROM documents.documents WHERE slug = 'slow-query-triage'),
        (SELECT id FROM documents.tags WHERE slug = 'performance')
    )
ON CONFLICT (document_id, tag_id) DO NOTHING;
