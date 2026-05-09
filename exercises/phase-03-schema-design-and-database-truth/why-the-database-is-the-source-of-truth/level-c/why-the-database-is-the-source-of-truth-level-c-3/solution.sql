DROP TABLE IF EXISTS ecommerce.why_the_database_is_the_source_of_truth_c_3;
CREATE TABLE ecommerce.why_the_database_is_the_source_of_truth_c_3 (
    id bigint generated always as identity PRIMARY KEY,
    email text,
    full_name text,
    imported_at timestamptz
);

ALTER TABLE ecommerce.why_the_database_is_the_source_of_truth_c_3
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN full_name SET NOT NULL,
    ALTER COLUMN imported_at SET DEFAULT now(),
    ALTER COLUMN imported_at SET NOT NULL;

ALTER TABLE ecommerce.why_the_database_is_the_source_of_truth_c_3
    ADD CONSTRAINT why_the_database_is_the_source_of_truth_c_3_email_unique UNIQUE (email);
