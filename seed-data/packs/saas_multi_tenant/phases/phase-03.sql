-- domain: saas_multi_tenant
-- phase: 03
-- depends: phase-02
-- description: tenant reference data and cross-tenant invariants

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS saas;

CREATE TABLE IF NOT EXISTS saas.countries (
    code text PRIMARY KEY,
    name text NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS saas.currencies (
    code text PRIMARY KEY,
    name text NOT NULL UNIQUE,
    minor_unit integer NOT NULL DEFAULT 2,
    CONSTRAINT currencies_minor_unit_check CHECK (minor_unit >= 0)
);

INSERT INTO saas.countries (code, name)
VALUES
    ('US', 'United States'),
    ('GB', 'United Kingdom')
ON CONFLICT (code) DO NOTHING;

INSERT INTO saas.currencies (code, name, minor_unit)
VALUES
    ('USD', 'US Dollar', 2),
    ('GBP', 'Pound Sterling', 2)
ON CONFLICT (code) DO NOTHING;

-- In phase 2, a tenant plan was just text and billing facts were absent. In
-- phase 3 we add country/currency reference columns, backfill, and enforce the
-- columns so future tenant rows cannot drift into spreadsheet-shaped text.
ALTER TABLE saas.tenants
    ADD COLUMN IF NOT EXISTS country_code text,
    ADD COLUMN IF NOT EXISTS billing_currency text;

UPDATE saas.tenants
SET country_code = 'US'
WHERE country_code IS NULL;

UPDATE saas.tenants
SET billing_currency = 'USD'
WHERE billing_currency IS NULL;

ALTER TABLE saas.tenants
    ALTER COLUMN slug SET NOT NULL,
    ALTER COLUMN name SET NOT NULL,
    ALTER COLUMN plan_name SET NOT NULL,
    ALTER COLUMN country_code SET DEFAULT 'US',
    ALTER COLUMN country_code SET NOT NULL,
    ALTER COLUMN billing_currency SET DEFAULT 'USD',
    ALTER COLUMN billing_currency SET NOT NULL;

ALTER TABLE saas.users
    ALTER COLUMN tenant_id SET NOT NULL,
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN full_name SET NOT NULL,
    ALTER COLUMN role_name SET NOT NULL;

ALTER TABLE saas.projects
    ALTER COLUMN tenant_id SET NOT NULL,
    ALTER COLUMN name SET NOT NULL,
    ALTER COLUMN status SET NOT NULL;

ALTER TABLE saas.project_memberships
    ALTER COLUMN tenant_id SET NOT NULL,
    ALTER COLUMN project_id SET NOT NULL,
    ALTER COLUMN user_id SET NOT NULL,
    ALTER COLUMN access_level SET NOT NULL;

DO $$
BEGIN
    ALTER TABLE saas.users
        ADD CONSTRAINT users_tenant_email_unique UNIQUE (tenant_id, email);
EXCEPTION
    WHEN duplicate_table OR duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE saas.projects
        ADD CONSTRAINT projects_tenant_name_unique UNIQUE (tenant_id, name);
EXCEPTION
    WHEN duplicate_table OR duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE saas.project_memberships
        ADD CONSTRAINT project_memberships_project_user_unique UNIQUE (project_id, user_id);
EXCEPTION
    WHEN duplicate_table OR duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE saas.project_memberships
        ADD CONSTRAINT project_memberships_access_level_check
        CHECK (access_level IN ('viewer', 'editor', 'admin'));
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE saas.tenants
        ADD CONSTRAINT tenants_country_code_fkey
        FOREIGN KEY (country_code) REFERENCES saas.countries(code);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE saas.tenants
        ADD CONSTRAINT tenants_billing_currency_fkey
        FOREIGN KEY (billing_currency) REFERENCES saas.currencies(code);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;
