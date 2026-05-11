# Range, List, and Hash Partitioning

## Problem Framing

Partitioning is an operational tool for a table whose lifecycle has become visible. In this phase the default question is not "can PostgreSQL partition this table?" but "what problem will partitioning remove from normal operations?" The event-heavy corpus uses `events.event_log_partitioned` because retention, hot/cold separation, and append-heavy maintenance are concrete. The ecommerce corpus keeps `ecommerce.orders` and adds `ecommerce.orders_partitioned` so learners can compare the partitioned shape against the simpler original. The working vocabulary for this lesson is range_partitioning, list_partitioning, hash_partitioning, partition key choice. A good design names the partition key, the retention window, the queries that should prune, and the maintenance work that becomes easier.

## Minimal Concept Introduction

Declarative partitioning routes rows from one logical parent table into child tables. Range partitioning fits time-series events and quarterly order history because predicates such as `event_time >= ... AND event_time < ...` map cleanly to partition bounds. List partitioning fits stable categories such as region or tenant tier. Hash partitioning spreads rows when there is no lifecycle boundary, but it rarely solves retention by itself. Partition pruning is the planner behavior that skips irrelevant child tables. Constraint exclusion is older planner vocabulary that still appears in some discussions, but declarative partitions primarily rely on partition pruning. Indexes on partitioned tables are not global indexes; PostgreSQL manages partitioned index definitions and physical child indexes.

## Worked Example

Use a date-bounded query before changing any schema. A learner should run `EXPLAIN` on `events.event_log_partitioned` with a narrow `event_time` window and verify that only matching monthly partitions appear. Then run a broad query or a predicate that wraps the partition key in a function and notice that pruning can disappear. The repair is often simple: compare the raw partition key to constants or parameters whose value PostgreSQL can reason about. For retention, create the next partition before the first write needs it, detach the oldest partition when the window expires, archive it if required, and drop it only after the retention decision is explicit.

## Diagnostic Questions

What operational pain exists today: slow deletes, vacuum pressure, backup scope, index rebuild time, or hot/cold data separation? Which predicates are common enough that pruning is measurable? Does the partition key appear naturally in those predicates? What happens to uniqueness when PostgreSQL requires the partition key to be part of a unique constraint on the parent? How will new partitions be created, old partitions detached, statistics refreshed, and failure noticed? If the answers are vague, the honest recommendation is "not yet" rather than premature partitioning.

## Common Pitfalls

The most common mistake is partitioning too early because a row count sounds large in isolation. Five hundred thousand rows with simple indexes, short retention, and no maintenance pain may be easier as one table. Another mistake is treating partitions as a magic performance button while queries still scan every partition. A third mistake is forgetting operational cost: every partition has indexes, statistics, privileges, backup behavior, and replica effects. A fourth mistake is assuming uniqueness works like a global index. If a unique constraint on a partitioned table omits the partition key, PostgreSQL rejects it on the parent; per-partition constraints can also create false confidence because duplicates may exist across partitions.

## Explain It Back

Explain the design as an on-call engineer. Name the parent table, child partition pattern, default partition purpose, pruning evidence, index plan, retention command, and rollback step. For `range-list-hash`, the important habit is to connect SQL syntax to operations. `ATTACH PARTITION` and `DETACH PARTITION` are not merely DDL verbs; they are lifecycle tools that change what normal queries read. A clear explanation also states when the design should be removed or simplified. Partitioning is successful when it makes retention and maintenance boring, not when it makes a schema look sophisticated.

## References and Further Reading

- `docs/partitioning-playbook.md` for authoring and retention templates.
- `docs/anti-patterns/partition_too_early.md` for premature partitioning review.
- `docs/indexing-playbook-part2.md` for partitioned-table index notes.
