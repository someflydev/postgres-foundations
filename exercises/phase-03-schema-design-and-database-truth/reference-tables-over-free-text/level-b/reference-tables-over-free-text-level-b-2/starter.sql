DROP TABLE IF EXISTS ecommerce.reference_tables_over_free_text_b_2;
DROP TABLE IF EXISTS ecommerce.reference_tables_over_free_text_b_2_statuses;
CREATE TABLE ecommerce.reference_tables_over_free_text_b_2_statuses (
    code text PRIMARY KEY,
    label text NOT NULL UNIQUE,
    is_terminal boolean NOT NULL DEFAULT false
);

CREATE TABLE ecommerce.reference_tables_over_free_text_b_2 (
    id bigint generated always as identity PRIMARY KEY,
    status_code text,
    description text NOT NULL
);

-- Add defaults, NOT NULL, and the foreign key below.
