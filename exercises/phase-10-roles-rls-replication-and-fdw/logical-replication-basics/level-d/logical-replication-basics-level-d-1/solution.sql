-- On the subscriber, inspect subscription health.
SELECT subname, subenabled
FROM pg_subscription
ORDER BY subname;

SELECT subname, status, received_lsn, latest_end_lsn, latest_end_time
FROM pg_stat_subscription
ORDER BY subname;

-- On the publisher, inspect slots and retained WAL.
SELECT slot_name,
       plugin,
       slot_type,
       active,
       restart_lsn,
       confirmed_flush_lsn,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained_wal
FROM pg_replication_slots
ORDER BY slot_name;

-- Diagnosis:
-- Logical replication can apply some changes while still falling farther
-- behind. A slot retains WAL needed by the subscriber. If the subscriber is
-- disabled, disconnected, schema-blocked, or too slow, retained WAL and catalog
-- cleanup pressure grow on the publisher.

-- Repair plan:
-- 1. Confirm whether the subscriber can catch up safely.
-- 2. Fix connectivity or schema mismatch if catch-up is intended.
-- 3. If abandoning the subscriber, drop the subscription from the subscriber so
--    PostgreSQL drops the publisher slot cleanly.
-- 4. Drop a publisher slot manually only after confirming no live subscriber
--    still depends on it.
