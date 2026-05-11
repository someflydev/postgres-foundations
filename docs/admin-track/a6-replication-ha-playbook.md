# A6 Replication and HA Operations Playbook

Replication operations start with the contract: physical replicas copy WAL for the cluster, while logical replication copies selected changes from publications to subscriptions. Monitor byte lag with `pg_wal_lsn_diff` and time lag with replay or apply timestamps. Zero byte lag is not enough if the relevant table is not part of the publication or the schema has drifted.

Failover checklist:

1. Confirm the primary failure and the target replica state.
2. Fence the old primary before promotion.
3. Promote with `pg_promote()` or the HA manager's equivalent.
4. Redirect clients and run application validation queries.
5. Preserve evidence for the postmortem.

Logical replication lifecycle work should plan initial sync, catch-up, replica identity, DDL compatibility, large transactions, and cutover/rollback. Near-zero-downtime major upgrades use those same mechanics with stricter validation gates.
