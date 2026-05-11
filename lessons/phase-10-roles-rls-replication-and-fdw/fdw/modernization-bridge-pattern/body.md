# Modernization Bridge Pattern

## Problem Framing

A modernization bridge is a deliberate intermediate state. The team has a
legacy shape that does not match the target model, but a full rewrite or cutover
is too risky. FDW can expose the old data to PostgreSQL while local tables add
mapping, validation, and new workflows. The pattern is not "pretend the legacy
system is gone." It is "make the boundary explicit so migration work can proceed
in small, observable steps."

## Minimal Concept Introduction

The Phase 10 modernization seed uses `legacy.crm_accounts_1998` and
`legacy.crm_notes_1998` to mimic an older source. It also has local mapping
tables such as `legacy.customer_mappings`. Foreign tables under `legacy_fdw`
let learners query the legacy rows through `postgres_fdw`. The bridge query
joins local mapping to foreign source rows. Over time, a real project might add
data-quality reports, backfill jobs, dual-write checks, or logical replication,
but the first step is often read-only federation with clear ownership.

## Worked Example

Join `legacy.customer_mappings` to `legacy_fdw.crm_accounts_1998` on the
external customer reference. The result shows which legacy accounts already map
to canonical customer references. Then find legacy accounts with no mapping.
That missing set is more valuable than a flashy abstraction: it tells the team
what data must be reconciled before cutover. Add `EXPLAIN VERBOSE` to see
whether a predicate on `cust_no` is pushed down to the remote table. If not,
rewrite the predicate so the remote side can do less work.

## Diagnostic Questions

Which system owns the source of truth today? Which local table records the
mapping decision? Which columns are legacy identifiers and which are canonical
identifiers? Is the bridge read-only or can it write back? What query proves the
bridge is useful? What query reveals unmapped or dirty data? What would make
FDW too slow or too coupled for the next phase?

## Common Pitfalls

The biggest pitfall is hiding legacy names too early. Renaming every field in a
view can make the old system look cleaner than it is and obscure migration
risks. Another pitfall is joining large local and foreign tables without a
pushdown-friendly predicate. A third is letting FDW become the permanent
architecture for a hot path without measuring latency and failure behavior.

## Explain It Back

Explain the bridge as a migration control point. Name the legacy table, foreign
table, local mapping table, canonical identifier, and unmapped-data report.
Then state the next decision: keep using FDW for exploration, materialize a
clean copy, add logical replication, or plan cutover. The right answer depends
on workload evidence, not on a preference for shiny migration patterns.

## References and Further Reading

- `docs/logical-replication-playbook.md` for when table-copy movement becomes relevant.
- `docs/domain-conventions.md` for reusable domain boundaries.
