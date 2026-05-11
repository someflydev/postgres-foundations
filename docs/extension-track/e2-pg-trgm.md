# E2 pg_trgm

`pg_trgm` adds character-trigram similarity for typo tolerance, fuzzy matching, and short-label search. It complements core full-text search; it does not replace lexical ranking, snippets, dictionaries, or field-aware document search.

Operational rules:

- Use `similarity()`, `word_similarity()`, and `%` only with thresholds that can be defended from examples.
- Prefer GIN trigram indexes for broad similarity and contains-style searches; consider GiST when distance ordering or signature tradeoffs matter.
- Keep btree indexes for prefix equality and `LIKE 'prefix%'` patterns that do not need fuzzy matching.
- Expect index size and write overhead, especially on frequently updated text columns.
- Move to Meilisearch, OpenSearch, or another search system only when relevance controls, analyzers, multi-index operations, or search-specific scale exceed what PostgreSQL should own.
