-- Diagnosis:
-- USING (true) authorizes every existing row covered by the policy. RLS is
-- enabled, but the policy predicate does not express tenant isolation.

SET ROLE saas_readonly;
SET app.tenant_id = '11111111-1111-1111-1111-111111111111';

-- Under the broken policy, this would return Acme rows while scoped to Northwind.
SELECT tenant_id, title
FROM saas.documents
WHERE tenant_id = '22222222-2222-2222-2222-222222222222'
ORDER BY title;

RESET ROLE;

DROP POLICY IF EXISTS tenant_isolation_select ON saas.documents;
CREATE POLICY tenant_isolation_select
    ON saas.documents
    FOR SELECT
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
