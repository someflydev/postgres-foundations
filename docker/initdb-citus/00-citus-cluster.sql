SELECT 'CREATE DATABASE pgfound OWNER pgfound'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'pgfound')\gexec

\connect pgfound

CREATE EXTENSION IF NOT EXISTS citus;
SELECT citus_set_coordinator_host('citus-coordinator', 5432);
SELECT citus_add_node('citus-worker-1', 5432);
SELECT citus_add_node('citus-worker-2', 5432);
