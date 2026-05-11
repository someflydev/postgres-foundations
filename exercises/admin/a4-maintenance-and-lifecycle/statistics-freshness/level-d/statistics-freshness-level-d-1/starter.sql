-- Collect the relevant PostgreSQL evidence first.
SELECT current_database(), current_user;
EXPLAIN SELECT * FROM saas.documents WHERE account_id = 1;
