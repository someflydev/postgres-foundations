# Vector before Lexical

The anti-pattern is adding embeddings before proving that lexical search failed. If users type words that appear in documents, start with core FTS. If they misspell names or search short fragments, test `pg_trgm`. pgvector becomes credible when users need meaning similarity, paraphrase retrieval, recommendations, or hybrid retrieval where lexical evidence is insufficient.

A premature vector design adds embedding generation, dimension choices, distance metrics, index build cost, recall tuning, and managed-service constraints. A responsible recommendation includes a lexical baseline, a semantic success criterion, and a not-yet trigger that sends the team back to FTS or trigrams.
