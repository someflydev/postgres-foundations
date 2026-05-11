-- domain: saas_multi_tenant
-- phase: 10
-- depends: phase-05
-- description: row-level security tables and tenant isolation policies

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS saas;

CREATE TABLE IF NOT EXISTS saas.documents (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id uuid NOT NULL REFERENCES saas.tenants(id),
    owner_user_id uuid REFERENCES saas.users(id),
    title text NOT NULL,
    body text NOT NULL,
    classification text NOT NULL DEFAULT 'internal',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT documents_classification_check
        CHECK (classification IN ('public', 'internal', 'restricted'))
);

CREATE TABLE IF NOT EXISTS saas.audit_events (
    id bigint generated always as identity PRIMARY KEY,
    tenant_id uuid NOT NULL REFERENCES saas.tenants(id),
    actor_user_id uuid REFERENCES saas.users(id),
    action text NOT NULL,
    target_table text NOT NULL,
    target_id text NOT NULL,
    occurred_at timestamptz NOT NULL DEFAULT now(),
    details jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS documents_tenant_id_id_idx
    ON saas.documents (tenant_id, id);

CREATE INDEX IF NOT EXISTS audit_events_tenant_occurred_idx
    ON saas.audit_events (tenant_id, occurred_at DESC);

INSERT INTO saas.documents (tenant_id, owner_user_id, title, body, classification)
SELECT tenant_id, id, title, body, classification
FROM (
    SELECT
        '11111111-1111-1111-1111-111111111111'::uuid AS tenant_id,
        u.id,
        'Northwind onboarding' AS title,
        'Tenant-scoped checklist for Northwind analysts.' AS body,
        'internal' AS classification
    FROM saas.users u
    WHERE u.email = 'owner@northwind.example'

    UNION ALL

    SELECT
        '11111111-1111-1111-1111-111111111111'::uuid AS tenant_id,
        u.id,
        'Northwind restricted pricing' AS title,
        'Restricted commercial notes for the Northwind account.' AS body,
        'restricted' AS classification
    FROM saas.users u
    WHERE u.email = 'analyst@northwind.example'

    UNION ALL

    SELECT
        '22222222-2222-2222-2222-222222222222'::uuid AS tenant_id,
        u.id,
        'Acme board metrics' AS title,
        'Tenant-scoped KPI narrative for Acme executives.' AS body,
        'internal' AS classification
    FROM saas.users u
    WHERE u.email = 'owner@acme.example'
) AS seed_rows
ON CONFLICT (id) DO NOTHING;

INSERT INTO saas.audit_events (tenant_id, actor_user_id, action, target_table, target_id, details)
SELECT
    d.tenant_id,
    d.owner_user_id,
    'document.created',
    'saas.documents',
    d.id::text,
    jsonb_build_object('title', d.title)
FROM saas.documents d
WHERE NOT EXISTS (
    SELECT 1
    FROM saas.audit_events existing
    WHERE existing.target_table = 'saas.documents'
      AND existing.target_id = d.id::text
      AND existing.action = 'document.created'
);

DO $$
BEGIN
    CREATE ROLE saas_app NOLOGIN;
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    CREATE ROLE saas_readonly NOLOGIN;
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

GRANT USAGE ON SCHEMA saas TO saas_app, saas_readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON saas.documents TO saas_app;
GRANT SELECT, INSERT ON saas.audit_events TO saas_app;
GRANT SELECT ON saas.documents, saas.audit_events TO saas_readonly;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA saas TO saas_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA saas
    GRANT SELECT ON TABLES TO saas_readonly;

ALTER TABLE saas.documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE saas.audit_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE saas.documents FORCE ROW LEVEL SECURITY;
ALTER TABLE saas.audit_events FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS tenant_isolation_select ON saas.documents;
CREATE POLICY tenant_isolation_select
    ON saas.documents
    FOR SELECT
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

DROP POLICY IF EXISTS tenant_isolation_modify ON saas.documents;
CREATE POLICY tenant_isolation_modify
    ON saas.documents
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id')::uuid)
    WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);

DROP POLICY IF EXISTS tenant_isolation_select ON saas.audit_events;
CREATE POLICY tenant_isolation_select
    ON saas.audit_events
    FOR SELECT
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

DROP POLICY IF EXISTS tenant_isolation_modify ON saas.audit_events;
CREATE POLICY tenant_isolation_modify
    ON saas.audit_events
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id')::uuid)
    WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);

-- Session scoping demo:
-- SET app.tenant_id = '11111111-1111-1111-1111-111111111111';
-- SELECT title FROM saas.documents ORDER BY title;
-- SET app.tenant_id = '22222222-2222-2222-2222-222222222222';
-- SELECT title FROM saas.documents ORDER BY title;
