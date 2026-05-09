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
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO saas.tenants (id, slug, name, plan_name)
VALUES
    ('33333333-3333-3333-3333-333333333333', 'emptyco', 'EmptyCo Trial', 'trial')
ON CONFLICT (slug) DO NOTHING;

INSERT INTO saas.projects (tenant_id, name, status)
VALUES
    ('33333333-3333-3333-3333-333333333333', 'Unstaffed launch', 'active')
ON CONFLICT (tenant_id, name) DO NOTHING;

INSERT INTO saas.project_memberships (tenant_id, project_id, user_id, access_level)
SELECT tenant_id::uuid, project_id, user_id, access_level
FROM (
    SELECT
        '11111111-1111-1111-1111-111111111111' AS tenant_id,
        p.id AS project_id,
        u.id AS user_id,
        'admin' AS access_level
    FROM saas.projects p
    INNER JOIN saas.users u
        ON u.tenant_id = p.tenant_id
       AND u.email = 'owner@northwind.example'
    WHERE p.tenant_id = '11111111-1111-1111-1111-111111111111'
      AND p.name = 'Inventory refresh'

    UNION ALL

    SELECT
        '22222222-2222-2222-2222-222222222222' AS tenant_id,
        p.id AS project_id,
        u.id AS user_id,
        'admin' AS access_level
    FROM saas.projects p
    INNER JOIN saas.users u
        ON u.tenant_id = p.tenant_id
       AND u.email = 'owner@acme.example'
    WHERE p.tenant_id = '22222222-2222-2222-2222-222222222222'
      AND p.name = 'Board metrics'
) AS membership
WHERE NOT EXISTS (
    SELECT 1
    FROM saas.project_memberships existing
    WHERE existing.project_id = membership.project_id
      AND existing.user_id = membership.user_id
      AND existing.access_level = membership.access_level
);
