-- domain: ecommerce
-- phase: 08
-- depends: phase-07b
-- description: product full-text search vectors and weighted search index

ALTER TABLE ecommerce.products
    ADD COLUMN IF NOT EXISTS brand text NOT NULL DEFAULT 'PGFound',
    ADD COLUMN IF NOT EXISTS description text NOT NULL DEFAULT 'PostgreSQL learning product for operators and developers.';

UPDATE ecommerce.products
SET brand = CASE
        WHEN sku LIKE 'BK-%' THEN 'Fieldbook Press'
        WHEN sku LIKE 'MUG-%' THEN 'PGFound Goods'
        ELSE 'PGFound Catalog'
    END,
    description = CASE
        WHEN sku LIKE 'BK-%' THEN 'A practical PostgreSQL guide for indexing, search, query plans, and operational review.'
        WHEN sku LIKE 'MUG-%' THEN 'A durable mug for Postgres teams studying full-text search and indexing.'
        ELSE 'A catalog item with PostgreSQL search, indexing, and ranking practice text.'
    END;

ALTER TABLE ecommerce.products
    ADD COLUMN IF NOT EXISTS product_search_vec tsvector GENERATED ALWAYS AS (
        setweight(to_tsvector('english', coalesce(name, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(brand, '')), 'B') ||
        setweight(to_tsvector('english', coalesce(description, '')), 'C')
    ) STORED;

CREATE INDEX IF NOT EXISTS products_product_search_vec_gin_idx
    ON ecommerce.products USING gin (product_search_vec);
