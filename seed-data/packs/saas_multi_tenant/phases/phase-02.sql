-- domain: saas_multi_tenant
-- phase: 02
-- depends: phase-01
-- description: memberships for tenant-safe joins

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS saas;

CREATE TABLE IF NOT EXISTS saas.project_memberships (
    id bigint generated always as identity PRIMARY KEY,
    tenant_id uuid NOT NULL REFERENCES saas.tenants(id),
    project_id bigint NOT NULL REFERENCES saas.projects(id),
    user_id bigint NOT NULL REFERENCES saas.users(id),
    access_level text NOT NULL DEFAULT 'viewer',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (project_id, user_id)
);

INSERT INTO saas.project_memberships (tenant_id, project_id, user_id, access_level)
VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT id FROM saas.projects WHERE tenant_id = '11111111-1111-1111-1111-111111111111' AND name = 'Inventory refresh'),
        (SELECT id FROM saas.users WHERE tenant_id = '11111111-1111-1111-1111-111111111111' AND email = 'owner@northwind.example'),
        'admin'
    ),
    (
        '22222222-2222-2222-2222-222222222222',
        (SELECT id FROM saas.projects WHERE tenant_id = '22222222-2222-2222-2222-222222222222' AND name = 'Board metrics'),
        (SELECT id FROM saas.users WHERE tenant_id = '22222222-2222-2222-2222-222222222222' AND email = 'owner@acme.example'),
        'admin'
    )
ON CONFLICT (project_id, user_id) DO NOTHING;
