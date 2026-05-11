# Bloat And How To See It

## Problem Framing

Bloat diagnosis starts with pg_stat_all_tables signals such as n_dead_tup, vacuum counts, analyze counts, and tuple churn. Extensions like pgstattuple can measure more directly, but the operational habit is to correlate stats with workload, age, and table size. In the administration track this is treated as production behavior, not a preference hidden in a generated file. The operator must be able to explain the boundary, show the catalog or configuration evidence, and choose the least surprising remediation. For this lesson the recurring vocabulary is pg_stat_all_tables, n_dead_tup, pgstattuple, bloat. Each term is tied to a concrete failure mode: an app that cannot connect, a role that can connect too broadly, a session that holds resources indefinitely, a backup that cannot be restored, or a maintenance process that is not keeping pace with churn.

## Minimal Concept Introduction

Start with the smallest observable unit. Authentication is a rule match, pooling is a state boundary, backup is a recoverable artifact, vacuum is tuple cleanup, statistics are planner inputs, and upgrades are controlled cluster replacement. PostgreSQL gives useful inspection surfaces, but they only help when the learner knows what question to ask. A good answer names the actor, the database object or connection path, the configuration involved, and the evidence that would convince another operator. This keeps the lesson PostgreSQL core-first and avoids magical explanations.

## Worked Example

In the lab, connect as `pgfound` and collect evidence before changing anything. For connection topics, inspect `pg_stat_activity`, `SHOW max_connections`, and relevant authentication or SSL settings. For backup and maintenance topics, capture row counts, `pg_stat_all_tables`, `pg_stat_user_tables`, or planner estimates before running the command. Then apply one narrow change: adjust a role, route through PgBouncer, run `ANALYZE`, take a dump, restore it, or document the upgrade posture. Finally, repeat the original observation and compare. This before-and-after record is the work product.

## Diagnostic Questions

- What exact session, role, database, table, or timeline is affected?
- Which PostgreSQL view, command, or log entry proves the current state?
- Is the proposed fix reversible, online, and scoped to the smallest surface?
- What user-visible failure would occur if this control were wrong?
- Which follow-up check would catch the same problem next time?

## Common Pitfalls

Do not rely on application logs alone when PostgreSQL can show the active sessions, rule parsing, restore contents, table statistics, or vacuum state. Do not raise `max_connections` as a first response to a connection storm without accounting for backend memory and CPU. Do not call a dump successful until a restore has been performed. Do not use VACUUM FULL casually on a hot table because it rewrites and blocks. Do not assume a pooler preserves session state in transaction pooling. Operational answers must include evidence, blast radius, and a rollback or drain path.

## Explain It Back

Explain this lesson as an incident note. State the symptom, the PostgreSQL mechanism, the command or catalog evidence, and the remediation. Include the phrase `pg_stat_all_tables` and at least one of `bloat` or `n_dead_tup` so the explanation remains anchored in the real feature. If a teammate could perform the same diagnosis from your note, the explanation is specific enough. If the note only says to restart the database or increase capacity, it is not yet an administration answer.

## References and Further Reading

- `docs/admin-track/a4-backup-and-upgrades-playbook.md` for the operational checklist and command patterns.
- `docs/lab.md` for Docker profiles used by the authentication, pooling, and restore drills.
- PostgreSQL documentation for the exact server version used in the lab.
