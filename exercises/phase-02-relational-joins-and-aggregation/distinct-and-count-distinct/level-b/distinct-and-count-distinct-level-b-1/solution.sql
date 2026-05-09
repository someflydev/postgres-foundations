SELECT t.slug, count(DISTINCT u.id) AS users FROM saas.tenants t LEFT JOIN saas.users u ON u.tenant_id = t.id GROUP BY t.slug ORDER BY t.slug;
