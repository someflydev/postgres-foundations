SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN ('ecommerce', 'scheduling', 'saas') ORDER BY table_schema, table_name LIMIT 10;
