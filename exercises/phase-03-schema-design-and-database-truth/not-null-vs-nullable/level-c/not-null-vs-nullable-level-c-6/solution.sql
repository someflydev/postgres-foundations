DROP TABLE IF EXISTS ecommerce.not_null_vs_nullable_c_6;
CREATE TABLE ecommerce.not_null_vs_nullable_c_6 (
    id bigint generated always as identity PRIMARY KEY,
    email text,
    full_name text,
    phone text,
    created_at timestamptz
);

UPDATE ecommerce.not_null_vs_nullable_c_6
SET created_at = now()
WHERE created_at IS NULL;

ALTER TABLE ecommerce.not_null_vs_nullable_c_6
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN full_name SET NOT NULL,
    ALTER COLUMN created_at SET DEFAULT now(),
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE ecommerce.not_null_vs_nullable_c_6
    ADD CONSTRAINT not_null_vs_nullable_c_6_email_unique UNIQUE (email);
