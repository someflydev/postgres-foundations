-- Publisher: run on pg.
SHOW wal_level;

DROP PUBLICATION IF EXISTS phase10_pub;
DROP TABLE IF EXISTS public.replication_lab_events;

CREATE TABLE public.replication_lab_events (
    id bigint PRIMARY KEY,
    event_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE PUBLICATION phase10_pub
    FOR TABLE public.replication_lab_events;

INSERT INTO public.replication_lab_events (id, event_name)
VALUES (1, 'publisher-ready');

-- Subscriber: run on pg-replica.
DROP SUBSCRIPTION IF EXISTS phase10_sub;
DROP TABLE IF EXISTS public.replication_lab_events;

CREATE TABLE public.replication_lab_events (
    id bigint PRIMARY KEY,
    event_name text NOT NULL,
    created_at timestamptz NOT NULL
);

CREATE SUBSCRIPTION phase10_sub
    CONNECTION 'host=pg port=5432 dbname=pgfound user=pgfound password=pgfound'
    PUBLICATION phase10_pub;

SELECT id, event_name
FROM public.replication_lab_events
ORDER BY id;

-- Publisher: run after the subscription exists.
INSERT INTO public.replication_lab_events (id, event_name)
VALUES (2, 'after-subscription');

-- Subscriber: verify catch-up.
SELECT id, event_name
FROM public.replication_lab_events
ORDER BY id;
