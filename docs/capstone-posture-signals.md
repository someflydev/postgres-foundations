# Capstone Posture Signals

The capstone reviewer emits extension-specific signals when a solution enables
or proposes an extension without the posture evidence expected by the
`extension-posture` rubric.

## Signals

- `postgis_without_justification`: fires when PostGIS appears in schema or
  index artifacts and the `Extension posture` writeup section has fewer than
  200 words. Reviewers should ask for workload-specific spatial requirements,
  core alternatives, operational cost, and progression triggers.
- `pgvector_without_lexical_baseline`: fires when pgvector or vector columns
  appear without a writeup comparison to both pg_trgm and full-text search.
  Reviewers should require a lexical baseline before accepting semantic search.
- `citus_without_distribution_key_justification`: fires when Citus is proposed
  without distribution-key reasoning. Reviewers should look for shard-local
  joins, tenant or time locality, co-location, and single-node limits.
- `timescale_without_partition_comparison`: fires when TimescaleDB is proposed
  without comparing it to core partitioning or pg_partman. Reviewers should ask
  whether compression, continuous aggregates, retention policies, or
  time-series ergonomics justify the dependency.

Each signal is mapped into the extension-posture dimension. A finding from one
of these signals should be treated as an actionable rewrite request, not a
style preference.
