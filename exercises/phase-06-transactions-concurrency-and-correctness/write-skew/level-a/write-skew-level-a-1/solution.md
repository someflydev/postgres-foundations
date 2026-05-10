# Reference Solution

A complete answer identifies the invariant, the concurrent statements that can violate it, and the PostgreSQL mechanism that protects it. The expected repair uses core PostgreSQL behavior from Phase 6: transaction boundaries, row locks, atomic updates, SERIALIZABLE retries, savepoints, or idempotent upsert patterns. Avoid future-phase indexing or partitioning explanations.
