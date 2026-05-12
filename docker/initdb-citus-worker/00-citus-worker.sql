SELECT 'CREATE DATABASE pgfound OWNER pgfound'
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'pgfound')\gexec

\connect pgfound

CREATE EXTENSION IF NOT EXISTS citus;
