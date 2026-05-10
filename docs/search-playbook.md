# Search Playbook

PostgreSQL search work should start with the question the user is actually asking. A lexical lookup, a typo-tolerant lookup, and a semantic similarity lookup are different workloads. Treating them as one feature usually produces a system that is harder to explain and harder to operate.

## Lexical Full-Text Search

Core PostgreSQL full-text search is the first stop for document and product search where users type words they expect to appear in the result. Phase 8 teaches `tsvector`, `tsquery`, language configurations, dictionaries, generated or trigger-maintained vectors, GIN indexes, `ts_rank`, `ts_rank_cd`, and `ts_headline`.

Use lexical FTS when exact words, stems, titles, bodies, tags, authors, and category filters matter. Store a weighted vector when ranking needs to favor a title hit over a body hit. Use `websearch_to_tsquery` or `plainto_tsquery` for user input rather than interpolating raw text into `to_tsquery`.

## Fuzzy Search Preview

`pg_trgm` helps when users misspell words, use partial fragments, or search short labels where stemming is not the issue. Phase 8 only previews this choice so learners can recognize the signal. The extension deep-dive arrives in Phase E2, PROMPT_34.

## Semantic Search Pointer

`pgvector` is useful when users need meaning similarity rather than lexical overlap: related concepts, paraphrases, recommendations, or embedding-backed retrieval. It is deliberately later, in Phase E4, PROMPT_35. Do not use vector search to skip basic lexical evidence.

## Not Yet Logic

Stay with core FTS when the workload is explainable as words in documents, ranking by fields, snippets, and ordinary filters. Reach for `pg_trgm` when typo tolerance is the missing capability. Reach for `pgvector` when meaning similarity is the requirement. Consider an external engine only when operators need search-specific scaling, analyzers, relevance controls, or multi-index operations that PostgreSQL cannot carry without becoming the wrong bottleneck.
