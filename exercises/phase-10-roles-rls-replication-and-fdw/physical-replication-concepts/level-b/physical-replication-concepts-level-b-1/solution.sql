-- Publisher on pg:
CREATE TABLE IF NOT EXISTS public.replication_lab_events (
    id bigint PRIMARY KEY,
    event_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE PUBLICATION phase10_pub FOR TABLE public.replication_lab_events;
-- Subscriber on pg-replica creates the same table, then CREATE SUBSCRIPTION with a pg connection string.
