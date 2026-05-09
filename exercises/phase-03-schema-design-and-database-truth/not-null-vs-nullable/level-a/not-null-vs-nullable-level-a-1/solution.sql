DROP TABLE IF EXISTS ecommerce.not_null_vs_nullable_a_1;
CREATE TABLE ecommerce.not_null_vs_nullable_a_1 (
    id bigint generated always as identity PRIMARY KEY,
    email text,
    full_name text,
    phone text,
    created_at timestamptz
);

UPDATE ecommerce.not_null_vs_nullable_a_1
SET created_at = now()
WHERE created_at IS NULL;

ALTER TABLE ecommerce.not_null_vs_nullable_a_1
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN full_name SET NOT NULL,
    ALTER COLUMN created_at SET DEFAULT now(),
    ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE ecommerce.not_null_vs_nullable_a_1
    ADD CONSTRAINT not_null_vs_nullable_a_1_email_unique UNIQUE (email);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce'
  AND table_name = 'not_null_vs_nullable_a_1'
ORDER BY table_name;
