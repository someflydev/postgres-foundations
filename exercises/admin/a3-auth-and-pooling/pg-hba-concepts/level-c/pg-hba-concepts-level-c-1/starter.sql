-- Collect the relevant PostgreSQL evidence first.
SELECT current_database(), current_user;
SELECT line_number, type, database, user_name, auth_method FROM pg_hba_file_rules;
