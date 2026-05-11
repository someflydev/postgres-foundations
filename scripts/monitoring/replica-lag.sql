-- Purpose: report physical sender lag and logical subscription lag in bytes and time when available.
-- On a primary, physical rows come from pg_stat_replication; on a subscriber, logical rows come from pg_stat_subscription.
SELECT
    'physical'::text AS replication_kind,
    application_name AS name,
    client_addr::text AS peer,
    state,
    sync_state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS byte_lag,
    write_lag,
    flush_lag,
    replay_lag,
    NULL::interval AS apply_time_lag
FROM pg_stat_replication
UNION ALL
SELECT
    'logical'::text AS replication_kind,
    subname AS name,
    NULL::text AS peer,
    'subscription'::text AS state,
    NULL::text AS sync_state,
    CASE
        WHEN received_lsn IS NULL THEN NULL
        ELSE pg_wal_lsn_diff(latest_end_lsn, received_lsn)
    END AS byte_lag,
    NULL::interval AS write_lag,
    NULL::interval AS flush_lag,
    NULL::interval AS replay_lag,
    now() - latest_end_time AS apply_time_lag
FROM pg_stat_subscription
ORDER BY replication_kind, name;
