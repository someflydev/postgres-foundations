-- domain: saas_multi_tenant
-- phase: 05
-- depends: phase-04a
-- expected rows: >= 50 tenants, each with 5-200 users, >= 6000 usage events
-- description: multi-tenant volume for lateral joins, windows, upserts, views, and rollups

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS saas;

WITH generated AS (
    SELECT gs,
           (substr(md5('phase5-tenant-' || gs), 1, 8) || '-' ||
            substr(md5('phase5-tenant-' || gs), 9, 4) || '-' ||
            substr(md5('phase5-tenant-' || gs), 13, 4) || '-' ||
            substr(md5('phase5-tenant-' || gs), 17, 4) || '-' ||
            substr(md5('phase5-tenant-' || gs), 21, 12))::uuid AS tenant_id
    FROM generate_series(1, 50) AS gs
)
INSERT INTO saas.tenants (id, slug, name, plan_name, country_code, billing_currency, settings)
SELECT tenant_id, format('phase5-tenant-%s', gs), format('Phase Five Tenant %s', gs),
       CASE WHEN gs % 10 = 0 THEN 'enterprise' WHEN gs % 3 = 0 THEN 'team' ELSE 'starter' END,
       'US', 'USD', jsonb_build_object('features', jsonb_build_object('usage_events', true), 'phase', 5)
FROM generated
ON CONFLICT (slug) DO UPDATE
SET plan_name = EXCLUDED.plan_name,
    settings = EXCLUDED.settings,
    updated_at = now();

WITH tenants AS (
    SELECT id, slug, row_number() OVER (ORDER BY slug) AS tenant_rn
    FROM saas.tenants
    WHERE slug LIKE 'phase5-tenant-%'
), generated AS (
    SELECT t.id AS tenant_id, t.slug, user_n
    FROM tenants t
    CROSS JOIN LATERAL generate_series(1, 5 + ((t.tenant_rn * 17) % 196)) AS user_n
)
INSERT INTO saas.users (tenant_id, email, full_name, role_name)
SELECT tenant_id,
       format('user-%s@%s.example', user_n, slug),
       format('User %s for %s', user_n, slug),
       CASE WHEN user_n = 1 THEN 'owner' WHEN user_n % 11 = 0 THEN 'admin' ELSE 'member' END
FROM generated
ON CONFLICT (tenant_id, email) DO NOTHING;

CREATE TABLE IF NOT EXISTS saas.usage_events (
    id bigint generated always as identity PRIMARY KEY,
    tenant_id uuid NOT NULL REFERENCES saas.tenants(id),
    user_id uuid REFERENCES saas.users(id),
    event_name text NOT NULL,
    occurred_at timestamptz NOT NULL,
    quantity integer NOT NULL DEFAULT 1,
    properties jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

WITH tenants AS (
    SELECT id, row_number() OVER (ORDER BY slug) AS tenant_rn
    FROM saas.tenants
    WHERE slug LIKE 'phase5-tenant-%'
), generated AS (
    SELECT t.id AS tenant_id,
           '2026-01-01 00:00:00+00'::timestamptz + ((event_n % 90) * interval '1 day') + ((event_n % 24) * interval '1 hour') AS occurred_at,
           CASE WHEN event_n % 5 = 0 THEN 'export_created'
                WHEN event_n % 3 = 0 THEN 'report_viewed'
                ELSE 'project_opened' END AS event_name,
           1 + (event_n % 4) AS quantity,
           event_n
    FROM tenants t
    CROSS JOIN generate_series(1, 120) AS event_n
)
INSERT INTO saas.usage_events (tenant_id, user_id, event_name, occurred_at, quantity, properties)
SELECT g.tenant_id,
       (SELECT u.id FROM saas.users u WHERE u.tenant_id = g.tenant_id ORDER BY u.email LIMIT 1),
       g.event_name,
       g.occurred_at,
       g.quantity,
       jsonb_build_object('sequence', g.event_n, 'source', 'phase5')
FROM generated g
WHERE NOT EXISTS (
    SELECT 1 FROM saas.usage_events existing
    WHERE existing.tenant_id = g.tenant_id
      AND existing.occurred_at = g.occurred_at
      AND existing.properties->>'sequence' = g.event_n::text
);
