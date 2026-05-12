ALTER TABLE bridge_ext.accounts ENABLE ROW LEVEL SECURITY;
CREATE POLICY accounts_tenant_policy ON bridge_ext.accounts
    USING (tenant_id = current_setting('app.tenant_id', true));

ALTER TABLE bridge_ext.orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY orders_tenant_policy ON bridge_ext.orders
    USING (account_id IN (
        SELECT account_id FROM bridge_ext.accounts
        WHERE tenant_id = current_setting('app.tenant_id', true)
    ));
