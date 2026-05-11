# Physical Replication Concepts

## Problem Framing

Physical replication is introduced in Phase 10 as vocabulary, not as an
operations lab. Learners need to understand the shape of the tradeoff before
the admin track handles backup, failover, monitoring, and upgrade runbooks.
Physical replication streams the database cluster's WAL and keeps another
cluster physically consistent with the primary. It is the basis for standby
servers and high-availability designs, but it is not a table-level integration
tool and it does not let the subscriber reshape data.

## Minimal Concept Introduction

PostgreSQL writes changes to WAL before they are considered durable. Physical
streaming replication sends WAL records to a standby, which replays them. A
standby may be hot, meaning it can serve read-only queries while replaying.
Replication can be asynchronous or synchronous. Asynchronous replication allows
the primary to commit before the standby has replayed the change, so data loss
is possible if the primary disappears at the wrong moment. Synchronous
replication can reduce that window but adds commit latency and operational
coupling.

## Worked Example

Use physical replication as a design discussion. If a SaaS team says "we need a
read replica for dashboard traffic," the right questions are about lag,
read-your-writes behavior, failover, backup, and connection routing. If the
team says "we need only audit events in another database," physical replication
is the wrong level; logical replication or a pipeline is closer. If the team
says "we want a standby we can promote if the primary dies," physical
replication is the relevant concept, but the implementation belongs to the
admin prompts.

## Diagnostic Questions

Is the desired copy cluster-wide or table-specific? Can the receiving side
change schema independently? How much lag is acceptable? Who promotes the
standby, and what happens to clients during failover? Are backups and restore
tests separate from replication? Is a read-only standby allowed to serve stale
results? What monitoring would reveal replay delay or a broken WAL stream?

## Common Pitfalls

The classic mistake is calling every copy a replica. A logical subscriber is
not a physical standby. An FDW foreign table is not replicated at all. Another
mistake is treating a standby as a backup; replication can faithfully copy bad
deletes and corrupt assumptions. Finally, failover is not automatic just
because WAL is streaming. Promotion, fencing, DNS or routing, and application
reconnect behavior are operational decisions.

## Explain It Back

Explain physical replication as WAL replay for a whole cluster. Name the
primary, standby, WAL stream, lag, and failover decision. Then state what it is
not: not selective table movement, not schema transformation, and not a
replacement for backup. A learner who can say that clearly is ready to compare
physical replication with the logical replication lab without mixing their
purposes.

## References and Further Reading

- `docs/logical-replication-playbook.md` for contrast with logical replication.
- `docs/lab.md` for the Phase 10 logical replication profile.
