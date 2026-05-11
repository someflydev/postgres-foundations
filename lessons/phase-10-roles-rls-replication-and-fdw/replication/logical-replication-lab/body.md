# Logical Replication Lab

## Problem Framing

The logical replication lab turns vocabulary into a running publisher and
subscriber. The Compose service `pg-replica` is deliberately not a physical
replica. It is a second independent PostgreSQL instance that receives table
changes through a subscription. That distinction matters: learners must create
the target table, create a publication on `pg`, create a subscription on
`pg-replica`, and observe catch-up. The lab is small so the operational shape is
visible.

## Minimal Concept Introduction

Both services start with `wal_level=logical`. The publisher is reachable as
`pg` inside the Compose network and as `localhost:55433` from the host. The
subscriber is reachable as `pg-replica` inside the network and `localhost:5435`
from the host. A publication is created on the publisher. A subscription is
created on the subscriber. Initial sync copies existing rows, and later inserts
stream through the replication slot. Cleanup should drop the subscription
before dropping the publication so the slot is released cleanly.

## Worked Example

Bring up the profile with `docker compose -f docker/docker-compose.yml --profile
replication up -d`. On `pg`, create `public.replication_lab_events`, create
`phase10_pub`, and insert `publisher-ready`. On `pg-replica`, create the same
table and then create `phase10_sub` using a connection string that points at
`host=pg`. Query the subscriber until the first row appears. Insert
`after-subscription` on the publisher and query again. A correct lab transcript
shows both rows on the subscriber and can name which row arrived through
initial sync versus ongoing streaming.

## Diagnostic Questions

Can the subscriber resolve `host=pg` from inside the Compose network? Did the
publisher table exist before the publication? Did the subscriber table exist
before the subscription? Does the user in the connection string have enough
privilege? Is a slot visible on the publisher? If the row is missing, is the
subscription disabled, still copying, blocked by schema mismatch, or unable to
connect?

## Common Pitfalls

Using `localhost` inside the subscription connection string points at the
subscriber container, not the publisher. Forgetting the subscriber table causes
initial sync errors. Reusing an old subscription name can leave confusing slot
state. Another pitfall is leaving the lab running and assuming the named volume
will reset itself; init scripts run only on an empty data directory.

## Explain It Back

Explain the lab as a two-node trace. State which SQL ran on `pg`, which SQL ran
on `pg-replica`, which network name connected the subscription, and what rows
proved catch-up. Then state the cleanup sequence. The learner should leave with
a mental model of the publication/subscription lifecycle rather than a memorized
command block.

## References and Further Reading

- `docs/lab.md` for the exact replication profile commands.
- `docs/logical-replication-playbook.md` for slot and lag notes.
