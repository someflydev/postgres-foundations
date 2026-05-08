-- domain: document_search
-- phase: 01
-- depends: none
-- description: minimal schema + small seed

CREATE SCHEMA IF NOT EXISTS documents;

CREATE TABLE IF NOT EXISTS documents.authors (
    id bigint generated always as identity PRIMARY KEY,
    display_name text NOT NULL UNIQUE,
    team_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS documents.documents (
    id bigint generated always as identity PRIMARY KEY,
    author_id bigint NOT NULL REFERENCES documents.authors(id),
    slug text NOT NULL UNIQUE,
    title text NOT NULL,
    body text NOT NULL,
    status text NOT NULL DEFAULT 'draft',
    published_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO documents.authors (display_name, team_name)
VALUES
    ('Platform Team', 'engineering'),
    ('Support Team', 'customer-success')
ON CONFLICT (display_name) DO NOTHING;

INSERT INTO documents.documents (author_id, slug, title, body, status, published_at)
VALUES
    (
        (SELECT id FROM documents.authors WHERE display_name = 'Platform Team'),
        'backup-checklist',
        'Backup checklist',
        'Take backups, verify restores, and record recovery expectations.',
        'published',
        '2026-04-01 10:00:00+00'
    ),
    (
        (SELECT id FROM documents.authors WHERE display_name = 'Support Team'),
        'slow-query-triage',
        'Slow query triage',
        'Collect the query, parameters, timing, and observed plan before changing indexes.',
        'published',
        '2026-04-02 11:00:00+00'
    )
ON CONFLICT (slug) DO NOTHING;
