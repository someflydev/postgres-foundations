\connect pgfound

CREATE ROLE replication_lab LOGIN REPLICATION PASSWORD 'replication_lab';

GRANT USAGE ON SCHEMA public TO replication_lab;
