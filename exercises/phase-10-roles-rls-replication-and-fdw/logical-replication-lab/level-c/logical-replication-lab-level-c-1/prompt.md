# Logical Replication Lab Level C1

## Setup

Start the replication profile:

```sh
docker compose -f docker/docker-compose.yml --profile replication up -d
```

Use `pg` as the publisher and `pg-replica` as the logical subscriber target.

## Task

Create a publication on pg and a subscription on pg-replica for
`public.replication_lab_events`.

1. On `pg`, verify `SHOW wal_level` returns `logical`.
2. Create the publisher table and `phase10_pub`.
3. Insert one row before creating the subscription.
4. On `pg-replica`, create the matching table and `phase10_sub`.
5. Verify the initial row arrives.
6. Insert a second row on `pg` and verify it arrives on `pg-replica`.

## Success Criteria

- Shows which SQL runs on the publisher and which SQL runs on the subscriber.
- Verifies both initial sync and later streaming.
- Names the cleanup sequence for the subscription, publication, and slot.
