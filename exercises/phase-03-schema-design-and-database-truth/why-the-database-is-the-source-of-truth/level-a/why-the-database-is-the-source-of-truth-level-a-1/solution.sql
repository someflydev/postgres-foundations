DROP TABLE IF EXISTS ecommerce.why_the_database_is_the_source_of_truth_a_1;
CREATE TABLE ecommerce.why_the_database_is_the_source_of_truth_a_1 (
    id bigint generated always as identity PRIMARY KEY,
    email text,
    full_name text,
    imported_at timestamptz
);

ALTER TABLE ecommerce.why_the_database_is_the_source_of_truth_a_1
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN full_name SET NOT NULL,
    ALTER COLUMN imported_at SET DEFAULT now(),
    ALTER COLUMN imported_at SET NOT NULL;

ALTER TABLE ecommerce.why_the_database_is_the_source_of_truth_a_1
    ADD CONSTRAINT why_the_database_is_the_source_of_truth_a_1_email_unique UNIQUE (email);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce'
  AND table_name = 'why_the_database_is_the_source_of_truth_a_1'
ORDER BY table_name;
