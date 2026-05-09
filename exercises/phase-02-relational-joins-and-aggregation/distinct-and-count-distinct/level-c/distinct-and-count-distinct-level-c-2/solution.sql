SELECT t.plan_name, count(DISTINCT u.id) AS users FROM saas.tenants t LEFT JOIN saas.users u ON u.tenant_id = t.id GROUP BY t.plan_name ORDER BY t.plan_name;
