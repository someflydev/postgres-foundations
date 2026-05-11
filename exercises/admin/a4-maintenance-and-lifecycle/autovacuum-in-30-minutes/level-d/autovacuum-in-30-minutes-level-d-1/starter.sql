-- Collect the relevant PostgreSQL evidence first.
SELECT current_database(), current_user;
SELECT pid, state, backend_xmin, query FROM pg_stat_activity WHERE backend_xmin IS NOT NULL;
