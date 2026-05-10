-- domain: ecommerce
-- phase: 04a
-- depends: phase-03
-- description: UUID, timestamptz, and JSONB modeling examples

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS ecommerce;

ALTER TABLE ecommerce.orders
    ADD COLUMN IF NOT EXISTS external_reference uuid DEFAULT gen_random_uuid(),
    ADD COLUMN IF NOT EXISTS metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    ADD COLUMN IF NOT EXISTS ordered_at timestamptz;

UPDATE ecommerce.orders
SET external_reference = gen_random_uuid()
WHERE external_reference IS NULL;

UPDATE ecommerce.orders
SET ordered_at = placed_at
WHERE ordered_at IS NULL;

ALTER TABLE ecommerce.orders
    ALTER COLUMN external_reference SET NOT NULL,
    ALTER COLUMN ordered_at SET DEFAULT now(),
    ALTER COLUMN ordered_at SET NOT NULL;

DO $$
BEGIN
    ALTER TABLE ecommerce.orders
        ADD CONSTRAINT orders_external_reference_unique UNIQUE (external_reference);
EXCEPTION
    WHEN duplicate_table OR duplicate_object THEN NULL;
END
$$;

ALTER TABLE ecommerce.customers
    ADD COLUMN IF NOT EXISTS profile jsonb NOT NULL DEFAULT '{}'::jsonb;

UPDATE ecommerce.customers
SET profile = CASE email
    WHEN 'ada@example.com' THEN '{"locale":"en-GB","preferences":{"newsletter":true,"theme":"dark"},"support_tier":"standard"}'::jsonb
    WHEN 'grace@example.com' THEN '{"locale":"en-US","preferences":{"newsletter":false},"favorite_category":"books"}'::jsonb
    WHEN 'lin@example.com' THEN '{"locale":"en-US","preferenes":{"newsletter":true},"shipping":{"default_country":"US"}}'::jsonb
    ELSE '{"locale":"en-US","notes":"imported profile with sparse keys"}'::jsonb
END
WHERE profile = '{}'::jsonb;

UPDATE ecommerce.orders
SET metadata = CASE order_number
    WHEN 'EC-1001' THEN '{"channel":"web","fraud":{"score":12,"provider":"clear-check"},"gift":false}'::jsonb
    WHEN 'EC-1002' THEN '{"channel":"marketplace","fraud":{"score":"low"},"shippping":{"priority":true}}'::jsonb
    WHEN 'EC-1003' THEN '{"channel":"web","campaign":"spring-sql","warehouse":{"pick_zone":"A7"},"gift":true}'::jsonb
    ELSE '{"channel":"unknown","legacy_import":true}'::jsonb
END
WHERE metadata = '{}'::jsonb;
