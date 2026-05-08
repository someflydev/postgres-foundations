-- domain: saas_multi_tenant
-- phase: 01
-- depends: none
-- description: minimal schema + small seed

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS saas;

CREATE TABLE IF NOT EXISTS saas.tenants (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    slug text NOT NULL UNIQUE,
    name text NOT NULL,
    plan_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS saas.users (
    id bigint generated always as identity PRIMARY KEY,
    tenant_id uuid NOT NULL REFERENCES saas.tenants(id),
    email text NOT NULL,
    full_name text NOT NULL,
    role_name text NOT NULL DEFAULT 'member',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, email)
);

CREATE TABLE IF NOT EXISTS saas.projects (
    id bigint generated always as identity PRIMARY KEY,
    tenant_id uuid NOT NULL REFERENCES saas.tenants(id),
    name text NOT NULL,
    status text NOT NULL DEFAULT 'active',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, name)
);

INSERT INTO saas.tenants (id, slug, name, plan_name)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'northwind', 'Northwind Labs', 'team'),
    ('22222222-2222-2222-2222-222222222222', 'acme', 'Acme Analytics', 'enterprise')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO saas.users (tenant_id, email, full_name, role_name)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'owner@northwind.example', 'Nina Owner', 'owner'),
    ('11111111-1111-1111-1111-111111111111', 'analyst@northwind.example', 'Noah Analyst', 'member'),
    ('22222222-2222-2222-2222-222222222222', 'owner@acme.example', 'Ari Owner', 'owner')
ON CONFLICT (tenant_id, email) DO NOTHING;

INSERT INTO saas.projects (tenant_id, name, status)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'Inventory refresh', 'active'),
    ('22222222-2222-2222-2222-222222222222', 'Board metrics', 'active')
ON CONFLICT (tenant_id, name) DO NOTHING;
