# Search Playbook

PostgreSQL search work should start with the question the user is actually asking. A lexical lookup, a typo-tolerant lookup, and a semantic similarity lookup are different workloads. Treating them as one feature usually produces a system that is harder to explain and harder to operate.

## Lexical Full-Text Search

Core PostgreSQL full-text search is the first stop for document and product search where users type words they expect to appear in the result. Phase 8 teaches `tsvector`, `tsquery`, language configurations, dictionaries, generated or trigger-maintained vectors, GIN indexes, `ts_rank`, `ts_rank_cd`, and `ts_headline`.

Use lexical FTS when exact words, stems, titles, bodies, tags, authors, and category filters matter. Store a weighted vector when ranking needs to favor a title hit over a body hit. Use `websearch_to_tsquery` or `plainto_tsquery` for user input rather than interpolating raw text into `to_tsquery`.

## Fuzzy Search Preview

`pg_trgm` helps when users misspell words, use partial fragments, or search short labels where stemming is not the issue. Phase 8 only previews this choice so learners can recognize the signal. The extension deep-dive is `docs/extension-track/e2-pg-trgm.md`, with authored lessons under `lessons/extensions/e2-pg-trgm/`.

## Semantic Search Pointer

`pgvector` is useful when users need meaning similarity rather than lexical overlap: related concepts, paraphrases, recommendations, or embedding-backed retrieval. It is deliberately later, in extension module E4. Do not use vector search to skip basic lexical evidence.

The extension deep-dive is `docs/extension-track/e4-pgvector.md`, with authored lessons under `lessons/extensions/e4-pgvector/`. Treat vector search as one retrieval signal, not as a replacement for filters, ranking, or lexical diagnostics. Hybrid designs should keep core FTS and trigram evidence visible, then add vector distance only where semantic recall changes the product outcome.

The lab seed uses deterministic fake embeddings when the `vector` extension is available. They are placeholders for mechanics: column type, distance operator, exact search, HNSW index, and recall experiments. They are not meaningful semantic vectors and should not be used as evidence that a production embedding model will behave the same way.

## Not Yet Logic

Stay with core FTS when the workload is explainable as words in documents, ranking by fields, snippets, and ordinary filters. Reach for `pg_trgm` when typo tolerance is the missing capability. Reach for `pgvector` when meaning similarity is the requirement. Consider an external engine only when operators need search-specific scaling, analyzers, relevance controls, or multi-index operations that PostgreSQL cannot carry without becoming the wrong bottleneck.
