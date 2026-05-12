# Observability Event Analytics Reference Writeup

## Modeling

Events are append-only facts keyed by event time, trace, service, severity, latency, and JSON attributes. Rollups are separate because dashboards should not repeatedly scan raw hot partitions for every aggregate.

## Partitioning

Daily partitions match the ingest rate and 30-day hot retention. pg_partman automates future partition creation and detach windows. Six-month cold retention should move detached partitions to cheaper storage or an analytics replica instead of keeping all raw events in the primary path.

## Indexes

BRIN on event_time fits append order and huge volume. Btree indexes support service-time dashboard queries and trace-time backtraces. Partial indexes on warning and error events serve incident triage without indexing every debug row twice.

## Operations

pg_stat_statements is used to separate high-call dashboards from ad-hoc incident queries. Operators check partition pruning, rows removed by filters, BRIN summaries, and hot partition bloat before changing schema.

## Extension posture

pg_partman is now because daily partition creation and retention are routine operational tasks at 300 million events per day. Core partitioning remains the storage model, so the design stays understandable and portable. BRIN is core and now because event time is naturally correlated with append order.

TimescaleDB is later, not now. The stated workload can be expressed with core partitions, BRIN, rollup tables, and pg_partman automation. TimescaleDB becomes justified if compression, continuous aggregates, retention policies, and time-bucket ergonomics materially reduce operational burden after the team has measured dashboard and retention pain. The comparison point is explicit: core partitioning plus rollups is sufficient until pg_stat_statements, storage growth, and maintenance windows show that policy automation and compression are worth the extra extension dependency.

Logical replication to an analytics replica is later but discussed. It is justified when support dashboards, BI tools, or ad-hoc trace analysis consume resources needed for ingest. It should not be the first response to missing indexes or bad partition pruning.

Citus is avoid for now because cross-shard incident traces and percentiles add distribution complexity. A distribution key by service would help some dashboards but hurt cross-service traces. A distribution key by trace would help incidents but weaken service dashboards. The current requirement needs a single-node operational design first.

## Not yet

Do not add TimescaleDB, Citus, or a separate analytics store until the core partition design has measured limits. The progression triggers are missed retention windows, unacceptable dashboard latency after rollups, or primary ingest contention from support analytics.

## Detailed defense

The observability workload is intentionally uncomfortable for a single PostgreSQL system. Three hundred million events per day is high enough that the design must be disciplined about ingest, partitioning, retention, and query boundaries. The goal is not to pretend PostgreSQL is a universal telemetry warehouse. The goal is to design the first operationally honest PostgreSQL-backed event store and to state exactly when the team should move beyond it.

Events are append-only facts. The schema stores event time, trace ID, service name, severity, latency, and JSON attributes. The relational columns support the dominant filters and joins. JSON attributes preserve variable event detail without forcing a schema migration for every service-specific field. That does not mean JSON is the primary query model. If an attribute becomes a common dashboard filter, the team should promote it to a typed column or a targeted generated column with an index.

The primary partition key is event_time because every retention and dashboard query is time-bounded. Hot retention is 30 days, cold retention is six months, and incident investigations start with a time window. Daily partitions are justified by the daily ingest volume. Monthly partitions would be too large for detach, backup, and emergency maintenance. Hourly partitions might produce too many child tables and too much catalog overhead. Daily is a defensible first balance for the stated volume.

pg_partman is a now decision because partition creation and retention are routine, recurring operational tasks. At this ingest rate, missing tomorrow's partition is not a minor inconvenience. It is an outage path. pg_partman automates future partition creation and can participate in retention detach workflows. The underlying storage remains core PostgreSQL partitioning, which keeps the design understandable and gives the team a manual fallback. The runbook should include checks for future partitions, late-arriving rows, and child-table index consistency.

BRIN is a core feature and a good fit for event_time. Append-heavy event data is naturally correlated with time, and BRIN indexes stay small even on huge partitions. BRIN will not replace targeted btree indexes for service-time or trace-time queries, but it gives the planner a cheap way to skip irrelevant page ranges for broad time-window scans. The team should monitor whether physical correlation degrades. If backfilled or late events become common, BRIN effectiveness may fall and the ingest path may need sorting or separate backfill partitions.

Btree indexes are intentionally narrow. Service-time supports dashboards such as "recent checkout errors" or "last hour of billing events." Trace-time supports incident backtraces across services. A partial index for warning and error events supports triage without duplicating every debug row in another index. The design avoids indexing arbitrary JSON attributes because that would multiply write cost and storage at the exact point where ingest volume is already the main risk.

Rollups are part of the model, not an afterthought. Support dashboards that ask for p95 latency by service should not repeatedly scan raw event partitions for common time buckets if the same results are requested every minute. The reference includes hourly service rollups. A production system might maintain minute, five-minute, and hourly rollups depending on dashboard needs. The key is to give each rollup a freshness contract and a rebuild path. A stale rollup with a clear timestamp is safer than an expensive raw query that threatens ingest.

Percentile queries deserve special attention. `percentile_cont` is clear and correct for a reference query, but it can be expensive over large windows. The first optimization is not automatically TimescaleDB. The first optimization is narrowing the time window, using rollups for dashboards, and separating ad-hoc investigations from repeated views. If approximate percentiles become acceptable, the team can evaluate a summary strategy. The capstone should force the learner to name the difference between exact incident analysis and dashboard approximations.

The cross-service trace query is the reason the design cannot optimize only for service-local dashboards. Incidents often involve several services. A trace_id index lets support reconstruct the path without scanning every service partition. This also shapes the Citus decision. A distribution key by service would make service dashboards local but can scatter trace queries. A distribution key by trace helps incidents but weakens service dashboards and rollups. Until the team proves a dominant shard-local pattern, distribution is premature.

Retention has two phases. Hot partitions remain online for 30 days because support and dashboards need direct access. Cold retention lasts six months, but cold does not have to mean equally fast on the primary. Old partitions can be detached, archived, compressed outside the primary path, or replicated to an analytics system. The important operational principle is to avoid massive deletes. Detach and archive are predictable. Deletes against billions of rows are not.

Downsampling is a data product decision. Raw events are needed for immediate incident backtraces, but dashboards often need counts, rates, and percentiles. The system should define which rollups survive beyond hot retention. For example, six months of hourly service counts and p95 latency may be enough for trend analysis even after raw event partitions move cold. If compliance or audit requires raw retention, that requirement must be named separately from support analytics.

pg_stat_statements is the first triage view because it identifies query families by total cost and frequency. A dashboard that runs every five seconds can dominate total time even if each call is fast. An ad-hoc trace query can have high mean time but low total impact. These are different problems. The runbook should group normalized queries by dashboard, incident, retention, and rollup maintenance so operators do not respond to every slow statement with the same index.

Partition pruning must be checked before index changes. If a recent-events query scans many partitions, the problem may be a missing or non-sargable event_time predicate. Adding indexes to every partition will not fix an application query that wraps event_time in a function or omits a bound. The runbook should include EXPLAIN checks for partition pruning and should treat unbounded event queries as defects unless they run against an offline analytics copy.

TimescaleDB is a serious candidate later, not a doctrine violation. It provides features that can matter for time-series workloads: hypertables, compression, retention policies, continuous aggregates, and time-bucket ergonomics. The reference does not enable it because core partitioning, BRIN, pg_partman, and explicit rollups cover the first required shape. The threshold for adopting TimescaleDB should be tied to measured operational pain: retention jobs are too fragile, compression would materially reduce cost, continuous aggregates would replace unreliable rollup code, or query ergonomics are causing repeated production defects.

The TimescaleDB comparison must include portability and team ownership. Some managed services support it; others do not, or support specific versions. Upgrades and extension behavior become part of the operational plan. If the team is small or managed-service portability is mandatory, those costs weigh heavily. If the team has strong database operations capacity and time-series features remove more complexity than they add, the decision can change. That is the now/later/avoid posture the prompt expects.

Logical replication to an analytics replica is a later or conditional move. It can protect ingest from support dashboards and BI queries. It also introduces replication slot monitoring, lag management, schema-change coordination, and failure modes where a stalled subscriber retains WAL. The trigger should be measured: support analytics causes primary resource contention, BI freshness requirements are clear, and the organization can operate replication. It should not be used to hide inefficient primary queries that lack time bounds or partition pruning.

Citus is avoid for now because distribution-key ambiguity is high. The workload has service-local dashboards, trace-local incident queries, time-window aggregates, and retention operations. No single key obviously makes all dominant paths local. Sharding before the workload is understood can lock the team into expensive cross-shard queries. Citus might become relevant if ingest or storage exceeds single-node limits and the team can prove a distribution key that preserves the main queries. Until then it is an operational distraction.

The schema also needs guardrails around severity and service identity. Severity is constrained to a known set in the reference, which helps partial indexes and dashboards. Service names should be controlled by a registry in a full implementation, because arbitrary service labels create fragmented metrics. Trace IDs should be generated consistently by upstream services. The database can index trace_id, but it cannot repair missing propagation discipline across the fleet.

Ingest reliability is outside the SQL files but central to the posture. At this volume, batch size, copy strategy, connection pooling, and retry behavior matter. Failed inserts should be visible. Late events should have a defined path. Backfills should not destroy BRIN locality or block hot ingest. A mature implementation may use staging tables and controlled moves into partitions. The capstone reference focuses on schema and review, but the runbook should make ingest ownership explicit.

The human support workflow should shape query limits. Recent events by service should require a service and a time window. Trace replay should require a trace ID. Percentile dashboards should use rollups or bounded windows. Ad-hoc raw scans should be privileged and observable. If support engineers need broad historical exploration, that is evidence for an analytics replica or external warehouse, not a reason to weaken the primary guardrails.

The final recommendation is a staged design. Use core PostgreSQL partitioning, BRIN, btree indexes, rollups, and pg_partman now. Discuss logical replication as the pressure valve for analytics load. Treat TimescaleDB as a later candidate with concrete triggers. Avoid Citus until distribution-key evidence exists. This gives learners an extension-aware answer that is neither anti-extension nor extension-first.

## Reviewer checklist

A reviewer should begin with boundedness. Every critical query should have a time window or a trace identifier. Recent-service queries need service and time filters. Percentile queries need bounded windows or rollups. Incident backtraces need trace IDs. If a learner submits broad scans over raw events as normal dashboard queries, the design does not respect the ingest scale.

The second review point is partition operation. Daily partitions are plausible for 300 million events per day, but the learner must explain creation, indexing, detach, cold retention, and backfill handling. A design that says "partition by time" without pg_partman maintenance and retention detail is not operationally complete. A design that uses partitions but writes queries that defeat pruning is also incomplete.

The third review point is index restraint. BRIN should serve event-time pruning. Btree indexes should serve service-time and trace-time access. JSON attributes should not receive broad indexes unless the workload proves a stable predicate. Event systems can be destroyed by well-intentioned indexes that make ingest too expensive.

The fourth review point is rollup honesty. Dashboards and incident analysis have different freshness and precision requirements. A good answer names which aggregates are precomputed, how often they refresh, and when raw scans are still acceptable. It should also distinguish exact percentile analysis from dashboard approximations.

The fifth review point is the TimescaleDB decision. The learner can choose later or now if the argument is strong, but they must compare against core partitioning and pg_partman. The answer should name compression, continuous aggregates, retention policy automation, portability, and team ownership. Treating TimescaleDB as automatic because the data has timestamps should be scored down.

Reviewers should also look for ingest isolation. The write path should not compete with expensive dashboard refreshes, unbounded support queries, or cold-retention exports. If the learner proposes synchronous rollup maintenance on every event insert, ask how that survives peak traffic. If they propose batch rollups, ask how failures are retried and how dashboard freshness is communicated. At this event volume, operational scheduling is part of schema design.

Finally, a strong answer names what PostgreSQL should not do. It should not be the only long-term store for every raw event if the organization needs broad historical exploration. It should not allow arbitrary JSON search over six months of raw data on the primary. It should not hide retention failures behind emergency deletes. Clear limits make the PostgreSQL design more credible, because they show when to use replicas, archives, or a dedicated analytics system.

The learner should also name service-level ownership. A platform team can provide tables, partitions, and indexes, but service teams must emit consistent trace IDs, severity values, and latency fields. If producers send malformed or high-cardinality attribute payloads, the database will inherit that disorder. The writeup should make producer contracts part of the operational posture so schema design and telemetry discipline reinforce each other.

That producer contract should include a review path for new high-volume event types. Before a service adds noisy debug payloads, the platform should know the expected rate, retention value, and query need. Otherwise the database becomes an unpriced dumping ground rather than an observability system with accountable ownership.
