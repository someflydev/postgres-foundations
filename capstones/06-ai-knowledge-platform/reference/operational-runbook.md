# Operational Runbook

Use pg_stat_statements to separate lexical, fuzzy, semantic, and hybrid latency. Track calls, mean time, total time, and rows.

When the embedding model changes, write new rows with the new model identifier, build a new HNSW index concurrently when supported by the environment, compare retrieval quality, switch reads, then remove stale embeddings after rollback windows close.

Reindex GIN and HNSW indexes only after measured bloat, planner drift, or model replacement. Keep FTS and pg_trgm as the baseline during vector incidents.
