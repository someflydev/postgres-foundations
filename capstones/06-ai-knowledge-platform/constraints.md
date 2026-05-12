# Constraints

- Core FTS, pg_trgm, and pgvector are required.
- Hybrid retrieval is required.
- HNSW indexing is required for embeddings.
- TimescaleDB and Citus are not allowed for the reference design.
- The operational runbook must cover embedding model changes and reindex posture.
