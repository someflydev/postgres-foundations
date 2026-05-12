# Solution

Recommend a downgrade to core FTS plus `pg_trgm` until the team shows semantic retrieval evidence. The symptoms are misspellings, short labels, and exact words in product text, so vector search adds embedding generation, index rebuilds, and recall debugging without solving a semantic problem. Prove it with `websearch_to_tsquery`, a trigram threshold test, and EXPLAIN output for the existing filters.
