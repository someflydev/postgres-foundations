ALTER TABLE saas.documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE saas.documents FORCE ROW LEVEL SECURITY;

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

SET ROLE saas_readonly;

SET app.tenant_id = '11111111-1111-1111-1111-111111111111';
SELECT count(*) AS northwind_visible
FROM saas.documents;

SELECT count(*) AS acme_rows_visible_while_scoped_to_northwind
FROM saas.documents
WHERE tenant_id = '22222222-2222-2222-2222-222222222222';

SET app.tenant_id = '22222222-2222-2222-2222-222222222222';
SELECT count(*) AS acme_visible
FROM saas.documents;

RESET ROLE;
