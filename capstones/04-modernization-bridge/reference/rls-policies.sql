ALTER TABLE new_service.tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE new_service.customer_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE new_service.local_orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenants_self_read ON new_service.tenants
    USING (id::text = current_setting('app.tenant_id', true));

CREATE POLICY customer_links_tenant_access ON new_service.customer_links
    USING (tenant_id::text = current_setting('app.tenant_id', true))
    WITH CHECK (tenant_id::text = current_setting('app.tenant_id', true));

CREATE POLICY local_orders_tenant_access ON new_service.local_orders
    USING (tenant_id::text = current_setting('app.tenant_id', true))
    WITH CHECK (tenant_id::text = current_setting('app.tenant_id', true));
