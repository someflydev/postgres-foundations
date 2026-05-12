# E4 pgvector

pgvector is for semantic retrieval: finding related meaning when word overlap is not enough. It comes after core full-text search and `pg_trgm`, because most product search failures are lexical, typo-tolerant, or metadata-filtering problems before they are embedding problems.

Use the separate `pgvector` Compose profile for labs: `docker compose --profile pgvector up -d pgvector` from the `docker/` directory. The image is pinned to `pgvector/pgvector:pg16`. The main `pg` service remains plain `postgres:16`; advanced users may run a custom local image, but the default keeps vector mechanics out of non-vector lessons.

The document-search seed includes a deterministic fake embedding when the `vector` extension is available. Those vectors are not meaningful semantic embeddings. They exist only so learners can practice column types, distance operators, exact search, HNSW indexes, hybrid retrieval, and recall diagnostics without shipping an embedding model.
