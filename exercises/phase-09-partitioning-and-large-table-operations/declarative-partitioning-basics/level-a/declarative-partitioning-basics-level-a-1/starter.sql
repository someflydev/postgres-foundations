SELECT schemaname, tablename
FROM pg_tables
WHERE schemaname IN ('events', 'ecommerce')
ORDER BY 1, 2;
