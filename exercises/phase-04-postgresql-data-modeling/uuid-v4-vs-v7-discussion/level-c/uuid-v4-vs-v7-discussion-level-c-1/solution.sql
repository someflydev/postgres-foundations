SELECT tenant_id, count(*) FROM scheduling.appointments GROUP BY tenant_id ORDER BY tenant_id;
