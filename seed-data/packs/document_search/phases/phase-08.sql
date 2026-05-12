    -- domain: document_search
    -- phase: 08
    -- depends: phase-02
    -- description: full-text search corpus, generated tsvectors, categories, and GIN indexes

CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE SCHEMA IF NOT EXISTS documents;

CREATE OR REPLACE FUNCTION documents.tags_to_search_text(tags text[])
RETURNS text
LANGUAGE sql
IMMUTABLE
PARALLEL SAFE
AS $$
    SELECT array_to_string(tags, ' ')
$$;

CREATE TABLE IF NOT EXISTS documents.docs (
        id uuid PRIMARY KEY,
        title text NOT NULL,
        body text NOT NULL,
        published_at timestamptz NOT NULL,
        author text NOT NULL,
        tags text[] NOT NULL DEFAULT '{}',
        search_vec tsvector GENERATED ALWAYS AS (
            setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
            setweight(to_tsvector('english', coalesce(author, '')), 'B') ||
            setweight(to_tsvector('english', coalesce(documents.tags_to_search_text(tags), '')), 'B') ||
            setweight(to_tsvector('english', coalesce(body, '')), 'C')
        ) STORED
    );

    CREATE TABLE IF NOT EXISTS documents.categories (
        id bigint generated always as identity PRIMARY KEY,
        slug text NOT NULL UNIQUE,
        label text NOT NULL,
        description text NOT NULL
    );

    CREATE TABLE IF NOT EXISTS documents.doc_categories (
        doc_id uuid NOT NULL REFERENCES documents.docs(id) ON DELETE CASCADE,
        category_id bigint NOT NULL REFERENCES documents.categories(id) ON DELETE CASCADE,
        PRIMARY KEY (doc_id, category_id)
    );

    CREATE INDEX IF NOT EXISTS docs_search_vec_gin_idx ON documents.docs USING gin (search_vec);
    CREATE INDEX IF NOT EXISTS docs_published_at_idx ON documents.docs (published_at DESC);
    CREATE INDEX IF NOT EXISTS doc_categories_category_doc_idx ON documents.doc_categories (category_id, doc_id);

    INSERT INTO documents.categories (slug, label, description)
    VALUES
        ('operations', 'Operations', 'Runbooks, restore checks, and daily operating practices.'),
        ('performance', 'Performance', 'Query planning, indexing, vacuum, and latency work.'),
        ('modeling', 'Modeling', 'Schema, JSONB boundary, and migration design notes.'),
        ('correctness', 'Correctness', 'Transactions, isolation, and repair guidance.'),
        ('search', 'Search', 'Lexical search, ranking, highlighting, and search tradeoffs.')
    ON CONFLICT (slug) DO UPDATE
    SET label = EXCLUDED.label,
        description = EXCLUDED.description;

    WITH generated AS (
        SELECT
            ('00000000-0000-0000-0000-' || lpad(series.n::text, 12, '0'))::uuid AS id,
            initcap(topic.topic) || ' ' || initcap(action.action) || ' ' || lpad(series.n::text, 4, '0') AS title,
            (
                'This document explains ' || topic.topic || ' for PostgreSQL teams. ' ||
                'Paragraph one describes the workload signal, the failure mode, and the operator question.' || E'

' ||
                'Paragraph two gives a concrete SQL practice for ' || topic.topic || ', including measurement, review, and rollback notes. ' ||
                'Postgres indexing examples appear throughout the corpus so lexical search has realistic repeated terms.' || E'

' ||
                'Paragraph three records follow-up checks for maintainers, including explain plans, ranking expectations, and portability concerns before adding external systems.'
            ) AS body,
            ('2026-04-01 12:00:00+00'::timestamptz + ((series.n % 28) * interval '1 day')) AS published_at,
            author.author,
            topic.tags,
            category.slug AS category_slug
        FROM generate_series(1, 5000) AS series(n)
        CROSS JOIN LATERAL (
            SELECT * FROM (VALUES
                (1, 'postgres indexing', ARRAY['postgres','indexing','operations']),
                (2, 'backup restore', ARRAY['backup','restore','operations']),
                (3, 'vacuum maintenance', ARRAY['vacuum','maintenance','performance']),
                (4, 'query planning', ARRAY['query','planning','indexing']),
                (5, 'tenant isolation', ARRAY['tenant','isolation','saas']),
                (6, 'jsonb boundaries', ARRAY['jsonb','modeling','boundaries']),
                (7, 'transaction safety', ARRAY['transaction','correctness','locks']),
                (8, 'search ranking', ARRAY['search','ranking','documents']),
                (9, 'schema migration', ARRAY['migration','schema','safety']),
                (10, 'observability metrics', ARRAY['observability','metrics','plans']),
                (11, 'connection pooling', ARRAY['pooling','connections','operations']),
                (12, 'incident review', ARRAY['incident','review','repair'])
            ) AS topics(ord, topic, tags)
            WHERE topics.ord = ((series.n - 1) % 12) + 1
        ) AS topic
        CROSS JOIN LATERAL (
            SELECT * FROM (VALUES
                (1, 'guide'), (2, 'checklist'), (3, 'runbook'),
                (4, 'field note'), (5, 'design review'), (6, 'operator memo')
            ) AS actions(ord, action)
            WHERE actions.ord = ((series.n * 7) % 6) + 1
        ) AS action
        CROSS JOIN LATERAL (
            SELECT * FROM (VALUES
                (1, 'Platform Team'), (2, 'Support Team'), (3, 'Data Team'),
                (4, 'Reliability Team'), (5, 'Education Team')
            ) AS authors(ord, author)
            WHERE authors.ord = (series.n % 5) + 1
        ) AS author
        CROSS JOIN LATERAL (
            SELECT * FROM (VALUES
                (1, 'operations'), (2, 'performance'), (3, 'modeling'), (4, 'correctness'), (5, 'search')
            ) AS categories(ord, slug)
            WHERE categories.ord = (series.n % 5) + 1
        ) AS category
    ), upserted AS (
        INSERT INTO documents.docs (id, title, body, published_at, author, tags)
        SELECT id, title, body, published_at, author, tags
        FROM generated
        ON CONFLICT (id) DO UPDATE
        SET title = EXCLUDED.title,
            body = EXCLUDED.body,
            published_at = EXCLUDED.published_at,
            author = EXCLUDED.author,
            tags = EXCLUDED.tags
        RETURNING id
    )
    INSERT INTO documents.doc_categories (doc_id, category_id)
    SELECT generated.id, categories.id
    FROM generated
    JOIN documents.categories AS categories ON categories.slug = generated.category_slug
    ON CONFLICT (doc_id, category_id) DO NOTHING;

    CREATE OR REPLACE FUNCTION documents.docs_search_vec_trigger()
    RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        NEW.search_vec :=
            setweight(to_tsvector('english', coalesce(NEW.title, '')), 'A') ||
            setweight(to_tsvector('english', coalesce(NEW.author, '')), 'B') ||
            setweight(to_tsvector('english', coalesce(documents.tags_to_search_text(NEW.tags), '')), 'B') ||
            setweight(to_tsvector('english', coalesce(NEW.body, '')), 'C');
        RETURN NEW;
    END;
    $$;

    COMMENT ON FUNCTION documents.docs_search_vec_trigger() IS
        'Lesson variant only: use this on a trigger-maintained copy of docs, not on the generated-column table.';

CREATE OR REPLACE FUNCTION documents.fake_embedding_text(input text)
RETURNS text
LANGUAGE sql
IMMUTABLE
PARALLEL SAFE
AS $$
    SELECT '[' || string_agg(
        to_char((((('x' || substr(md5(coalesce(input, '') || ':' || dim::text), 1, 8))::bit(32)::bigint % 2001) - 1000)::numeric / 1000), 'FM0.000'),
        ',' ORDER BY dim
    ) || ']'
    FROM generate_series(1, 16) AS dims(dim)
$$;

COMMENT ON FUNCTION documents.fake_embedding_text(text) IS
    'Deterministic placeholder vector text for pgvector mechanics. These values are not semantic embeddings.';

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_available_extensions WHERE name = 'vector') THEN
        CREATE EXTENSION IF NOT EXISTS vector;
        EXECUTE 'ALTER TABLE documents.docs ADD COLUMN IF NOT EXISTS fake_embedding vector(16)';
        EXECUTE 'UPDATE documents.docs SET fake_embedding = documents.fake_embedding_text(title || '' '' || body)::vector WHERE fake_embedding IS NULL';
        EXECUTE 'CREATE INDEX IF NOT EXISTS docs_fake_embedding_hnsw_idx ON documents.docs USING hnsw (fake_embedding vector_cosine_ops)';
        COMMENT ON COLUMN documents.docs.fake_embedding IS
            'Deterministic fake embedding for pgvector labs only; not a meaningful semantic vector.';
    END IF;
END;
$$;
