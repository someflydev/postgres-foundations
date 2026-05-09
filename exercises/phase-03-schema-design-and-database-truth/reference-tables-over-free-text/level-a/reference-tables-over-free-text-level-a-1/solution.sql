DROP TABLE IF EXISTS ecommerce.reference_tables_over_free_text_a_1;
DROP TABLE IF EXISTS ecommerce.reference_tables_over_free_text_a_1_statuses;
CREATE TABLE ecommerce.reference_tables_over_free_text_a_1_statuses (
    code text PRIMARY KEY,
    label text NOT NULL UNIQUE,
    is_terminal boolean NOT NULL DEFAULT false
);

CREATE TABLE ecommerce.reference_tables_over_free_text_a_1 (
    id bigint generated always as identity PRIMARY KEY,
    status_code text,
    description text NOT NULL
);

ALTER TABLE ecommerce.reference_tables_over_free_text_a_1
    ALTER COLUMN status_code SET DEFAULT 'draft',
    ALTER COLUMN status_code SET NOT NULL;

ALTER TABLE ecommerce.reference_tables_over_free_text_a_1
    ADD CONSTRAINT reference_tables_over_free_text_a_1_status_code_fkey
    FOREIGN KEY (status_code) REFERENCES ecommerce.reference_tables_over_free_text_a_1_statuses(code);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce'
  AND table_name = 'reference_tables_over_free_text_a_1'
ORDER BY table_name;
