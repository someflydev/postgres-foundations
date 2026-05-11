CREATE ROLE replication_lab LOGIN REPLICATION PASSWORD 'replication_lab';

CREATE TABLE IF NOT EXISTS public.replication_lab_events (
    id bigint PRIMARY KEY,
    event_name text NOT NULL,
    created_at timestamptz NOT NULL
);

GRANT ALL PRIVILEGES ON TABLE public.replication_lab_events TO pgfound;
