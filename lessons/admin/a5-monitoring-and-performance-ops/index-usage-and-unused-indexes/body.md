# Index Usage And Unused Indexes

## Problem Framing

Index usage review keeps write cost honest. An index with no scans is not automatically bad, but it becomes a drop candidate when age, constraint status, workload coverage, and release rollback options all line up. The practical question is not whether a catalog view exists; it is what decision the view supports when the system is under pressure. A PostgreSQL operator should be able to collect evidence, name the risk, choose a bounded action, and describe how to verify the result. That habit keeps monitoring, performance triage, replication, and high-availability work connected to user-visible service behavior instead of isolated command memorization.

For this lesson the required vocabulary is: pg_stat_user_indexes, unused indexes, candidates for drop, idx_scan. Use those terms in incident notes exactly enough that another operator could rerun the same evidence query and reach the same conclusion. If a metric or catalog row is ambiguous, say what additional observation would disambiguate it.

## Minimal Concept Introduction

PostgreSQL exposes operational truth through system views, statistics collectors, WAL positions, lock state, and normal SQL functions. The useful pattern is stable: establish the symptom, query the closest catalog source, compare it to a recent baseline or expectation, and avoid broad changes until the evidence points at a narrow cause. This is especially important for administration work because many fixes have secondary cost. Dropping an index can speed writes and break a rare read path. Cancelling a backend can clear a queue and abort the wrong business workflow. Promoting a replica can restore service and create split-brain if the old primary is not fenced.

## Worked Example

Start with the smallest report that answers the operational question. Capture the database name, current time, the relevant relation or backend identifiers, and the metric that changed. If the issue is query performance, pair pg_stat_statements ranking with EXPLAIN (ANALYZE, BUFFERS) for one representative statement. If the issue is blocking, pair pg_stat_activity with pg_blocking_pids() and identify the blocker before cancelling anything. If the issue is replication, compare byte lag with time lag and confirm that the relevant publication or subscription actually includes the table whose freshness matters.

A good report has three lines of reasoning: before-state evidence, proposed action, and after-state verification. For example, a weekly triage note should list the top 5 by total time, one candidate whose mean time or I/O changed materially, the query text fingerprint, and the next measurement. A failover note should name the chosen target, the fencing step for the old primary, and the application validation query.

## Diagnostic Questions

What is the exact invariant that appears threatened: latency, freshness, capacity, durability, access, or availability? Which PostgreSQL view or function is closest to that invariant? Is the signal a point-in-time fact, an accumulated counter, or a rate that needs a time window? What is normal for this database at this hour? Which remediation changes user-visible behavior, and which only improves observability?

## Common Pitfalls

Do not treat a single counter as a complete diagnosis. An unused index may be needed for a constraint or a monthly report. Zero byte replica lag can still be wrong when logical replication excludes the relevant table after schema drift. A lock wait can be caused by a harmless transaction that should finish shortly or by an abandoned session that should be cancelled. Alert rules that fire on normal checkpoint spikes or expected maintenance windows create fatigue.

Also avoid hiding uncertainty. It is better to write that the evidence is consistent with I/O pressure but not yet proven than to invent confidence. Operators build trust by making the next check explicit.

## Explain It Back

Explain the diagnostic path in plain operational language. Name the source of evidence, what it proves, what it does not prove, the action you would take first, and the verification query or metric you would watch afterward. When the safest answer is "not yet", say what signal would change the decision.

## References and Further Reading

Use the PostgreSQL manuals for catalog definitions and the local admin playbooks for lab workflow. Prefer core PostgreSQL views and functions first. External dashboards, HA managers, and exporters are valuable after the core signal is understood, but they should not replace the operator's ability to explain the underlying database state.
