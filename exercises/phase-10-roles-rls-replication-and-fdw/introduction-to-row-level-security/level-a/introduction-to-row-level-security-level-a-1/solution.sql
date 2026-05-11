-- Reference shape: tenant-scoped RLS policy using a session claim.
ALTER TABLE saas.documents ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS tenant_isolation_select ON saas.documents;
CREATE POLICY tenant_isolation_select ON saas.documents
    FOR SELECT
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
SET app.tenant_id = '11111111-1111-1111-1111-111111111111';
SELECT tenant_id, title FROM saas.documents ORDER BY title;
