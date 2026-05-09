DROP TABLE IF EXISTS ecommerce.uniqueness_beyond_primary_key_a_1;
CREATE TABLE ecommerce.uniqueness_beyond_primary_key_a_1 (
    id bigint generated always as identity PRIMARY KEY,
    professional_id bigint,
    starts_at timestamptz,
    client_email text
);

ALTER TABLE ecommerce.uniqueness_beyond_primary_key_a_1
    ALTER COLUMN professional_id SET NOT NULL,
    ALTER COLUMN starts_at SET NOT NULL,
    ALTER COLUMN client_email SET NOT NULL;

ALTER TABLE ecommerce.uniqueness_beyond_primary_key_a_1
    ADD CONSTRAINT uniqueness_beyond_primary_key_a_1_professional_starts_unique UNIQUE (professional_id, starts_at);

ALTER TABLE ecommerce.uniqueness_beyond_primary_key_a_1
    ADD CONSTRAINT uniqueness_beyond_primary_key_a_1_client_email_unique UNIQUE (client_email);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce'
  AND table_name = 'uniqueness_beyond_primary_key_a_1'
ORDER BY table_name;
