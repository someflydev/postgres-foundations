-- domain: saas_multi_tenant
-- phase: 04a
-- depends: phase-03
-- description: UUID tenant and user identity with JSONB settings

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS saas;

ALTER TABLE saas.tenants
    ADD COLUMN IF NOT EXISTS settings jsonb NOT NULL DEFAULT '{}'::jsonb;

UPDATE saas.tenants
SET settings = CASE slug
    WHEN 'northwind' THEN '{"features":{"audit_log":true,"exports":"csv"},"timezone":"America/Chicago"}'::jsonb
    WHEN 'acme' THEN '{"features":{"audit_log":true,"sso":true},"timezone":"Europe/London","limits":{"projects":50}}'::jsonb
    WHEN 'emptyco' THEN '{"features":{"auditlog":false},"timezone":null,"trial":{"expires_on":"2026-06-01"}}'::jsonb
    ELSE '{"features":{},"source":"legacy"}'::jsonb
END
WHERE settings = '{}'::jsonb;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'saas'
          AND table_name = 'users'
          AND column_name = 'id'
          AND data_type <> 'uuid'
    ) THEN
        ALTER TABLE saas.users
            ADD COLUMN IF NOT EXISTS uuid_id uuid DEFAULT gen_random_uuid();

        UPDATE saas.users
        SET uuid_id = gen_random_uuid()
        WHERE uuid_id IS NULL;

        ALTER TABLE saas.users
            ALTER COLUMN uuid_id SET NOT NULL;

        ALTER TABLE saas.project_memberships
            ADD COLUMN IF NOT EXISTS user_uuid uuid;

        UPDATE saas.project_memberships AS membership
        SET user_uuid = users.uuid_id
        FROM saas.users
        WHERE users.id = membership.user_id
          AND membership.user_uuid IS NULL;

        ALTER TABLE saas.project_memberships
            ALTER COLUMN user_uuid SET NOT NULL;

        ALTER TABLE saas.project_memberships
            DROP CONSTRAINT IF EXISTS project_memberships_user_id_fkey,
            DROP CONSTRAINT IF EXISTS project_memberships_project_user_unique;

        ALTER TABLE saas.users
            DROP CONSTRAINT IF EXISTS users_pkey;

        ALTER TABLE saas.users
            RENAME COLUMN id TO legacy_id;

        ALTER TABLE saas.users
            RENAME COLUMN uuid_id TO id;

        ALTER TABLE saas.project_memberships
            RENAME COLUMN user_id TO legacy_user_id;

        ALTER TABLE saas.project_memberships
            RENAME COLUMN user_uuid TO user_id;

        ALTER TABLE saas.users
            ADD CONSTRAINT users_pkey PRIMARY KEY (id);

        ALTER TABLE saas.project_memberships
            ADD CONSTRAINT project_memberships_user_id_fkey
            FOREIGN KEY (user_id) REFERENCES saas.users(id);

        ALTER TABLE saas.project_memberships
            ADD CONSTRAINT project_memberships_project_user_unique
            UNIQUE (project_id, user_id);
    END IF;
END
$$;

DO $$
BEGIN
    ALTER TABLE saas.users
        ADD CONSTRAINT users_email_lower_check CHECK (email = lower(email));
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;
