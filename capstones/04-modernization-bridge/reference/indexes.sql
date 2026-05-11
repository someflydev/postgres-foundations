CREATE INDEX customer_links_tenant_legacy_idx
    ON new_service.customer_links (tenant_id, legacy_customer_id);

CREATE INDEX customer_links_legacy_idx
    ON new_service.customer_links (legacy_customer_id);

CREATE INDEX local_orders_tenant_created_idx
    ON new_service.local_orders (tenant_id, created_at DESC);

CREATE UNIQUE INDEX legacy_customer_order_totals_customer_idx
    ON new_service.legacy_customer_order_totals (legacy_customer_id);
