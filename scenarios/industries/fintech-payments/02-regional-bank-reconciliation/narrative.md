# Regional bank reconciliation platform

Regional bank reconciliation platform is a mid-stage pressure judgment brief from a team
of 34 engineers working in fintech payments. The product serves operators who live in
PostgreSQL-backed workflows every day: support staff, finance reviewers, compliance
analysts, and customer-facing teams who need answers while the business is open. The
current system runs on logical replication pair with PostgreSQL as the operational
source of truth. Largest tables include transactions (39,000,000 rows), ledger_entries
(118,000,000 rows), reconciliation_diffs (9,000,000 rows). Peak traffic is roughly 1900
read queries per second, 520 writes per second, and 430 database connections during busy
windows.

The operational tolerance is explicit: medium tolerance for pages, limited appetite for
bespoke operations, and a preference for changes that can be rehearsed during business
hours. The team is on aws_rds, any_managed and plans to stay in managed PostgreSQL
unless the evidence is overwhelming. They want decisions that keep restore, upgrade,
monitoring, and rollback paths understandable to the people who will actually own them.
A recommendation that depends on heroic manual intervention is not acceptable, even when
the feature looks attractive on a whiteboard.

The tenancy model is single tenant. The data shape mix is relational_core,
append_only_events, foreign_postgres_access, and the workload patterns are oltp_heavy,
append_heavy, analytics_adjacent, migration_bridge. The growth horizon is concrete: in 6
months the team expects to absorb the next customer or seasonal cycle, in 12 months they
expect current hot tables to roughly follow 8 percent month-over-month growth unless
product scope narrows, and in 24 months they expect today's borderline decisions to
become operational constraints. The known pending decision is this: They are evaluating
postgres_fdw for a legacy settlement database and logical replication for a staged
cutover.

The scenario is not a textbook case. The legacy database has settlement codes that
change after bank holidays, so federation must prove pushdown and consistency rather
than merely connect. The team has enough PostgreSQL skill to use indexes, constraints,
RLS, replication, and managed extensions, but not enough spare capacity to adopt every
specialized tool at once. The expected answer should separate core-first moves from
extension candidates and should say what evidence would change the recommendation. The
reader should have to weigh portability, tenant boundaries, audit expectations, and
scale signals rather than simply enabling a named extension.

The brief should be used in lessons, interviews, and capstones as a realistic planning
artifact. A strong response will ask for workload evidence, identify the operational
owner for any new feature, and preserve the ability to run restore drills. A weak
response will overfit to the largest number in the brief, ignore managed-service
constraints, or suggest a distributed topology before proving that the workload has a
stable distribution key and a team ready to operate it. The scenario deliberately leaves
a few unresolved facts so learners must ask follow-up questions instead of pretending
the report is complete.

## Operating Notes

The team has weekly change windows, but the practical rollback story is still uneven. Schema changes are reviewed by senior engineers, data backfills are rehearsed on snapshots when time allows, and index builds are scheduled around customer traffic. Observability is improving but not yet complete: slow query samples exist, connection counts are watched, and application traces identify a few hot endpoints, but nobody can yet explain every spike from database evidence alone. That gap is part of the exercise. Learners should decide what evidence must be gathered before recommending a bigger topology or a specialized extension.

The portability constraint is not a formality. Procurement, compliance, and staffing all point toward managed PostgreSQL for the next planning horizon. A solution that works only on a niche managed service, requires privileged host access, or needs a team to operate a separate cluster should be treated as a later-stage option unless the workload signal is overwhelming. The team is willing to use PostgreSQL extensions when they are available in the managed environment and when restore drills, upgrade plans, and ownership are explicit.

The 6-month goal is to stabilize the current product surface without adding a second operational database. The 12-month goal is to absorb growth while preserving auditability and readable incident response. The 24-month goal is to keep the architecture from closing off future choices: partitioning should not be adopted before retention and pruning are clear, search should not skip lexical baselines, distributed PostgreSQL should not appear before distribution-key evidence, and read replicas should not hide inefficient queries. The right answer should describe what to do now, what to measure next, and what would make a deferred recommendation become appropriate.

There are human constraints as well. Product managers want visible improvements, support teams need explainable behavior during customer escalations, and finance or compliance stakeholders may demand repeatable reports even when they are not latency-sensitive. The database plan must therefore handle correctness, operational load, and communication. A polished recommendation names the owning team, states the failure mode it reduces, and identifies the runbook or test that proves the recommendation is ready for production.
