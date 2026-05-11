# Logical Replication Playbook

Logical replication copies table changes through publications and
subscriptions. It is useful for selective data movement, upgrades, reporting
copies, and migration bridges. It is not a transparent physical standby and it
does not remove the need to understand keys, slots, privileges, lag, and DDL.

## Authoring Checklist

1. Confirm the publisher runs with `wal_level=logical`.
2. Create or choose a role the subscriber can use to connect to the publisher.
3. Ensure replicated tables have stable primary keys or replica identity rules.
4. Create a publication on the publisher for the intended tables.
5. Create matching schemas and tables on the subscriber.
6. Create the subscription on the subscriber.
7. Insert a small row on the publisher and verify it arrives on the subscriber.
8. Inspect lag and slot state before declaring the lab complete.

## Operational Notes

Replication slots retain WAL until the consumer confirms receipt. A stopped or
lagging subscriber can therefore grow storage pressure on the publisher. Initial
sync copies existing table data before streaming later changes. Schema changes
need separate planning because logical replication is table-data movement, not
full cluster replay. During upgrades, verify publications, subscriptions, slot
names, and replica identity before cutting traffic over.

The Phase 10 Docker profile starts a second independent PostgreSQL instance
named `pg-replica`; it is a logical subscriber target, not a physical replica.
That distinction is deliberate so learners can create a publication on `pg`,
create a subscription on `pg-replica`, and observe table-level catch-up.
