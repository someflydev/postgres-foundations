# Multi Language And Unaccent

## Problem Framing
The unaccent extension can fold cafe and café before lexeme parsing when that is what users expect. The document_search corpus gives learners thousands of rows, categories, authors, tags, and publication dates, so the lesson is not a toy string comparison. The default posture is PostgreSQL core first: prove that lexical search, ranking, snippets, and filters work before introducing another moving part. A good search decision names the user behavior, the corpus size, the update rate, and the operational owner.

## Minimal Concept Introduction
The lesson centers on unaccent, multi_language_search, search_configuration. In PostgreSQL, text search is built from parsed tokens, normalized lexemes, and `tsquery` expressions that match those lexemes. The important habit is to inspect the intermediate value instead of treating search as magic. Use `to_tsvector('english', text)` to see the lexemes, use `websearch_to_tsquery` for user-shaped input, and keep raw Boolean `to_tsquery` for controlled expressions where syntax errors are acceptable feedback.

## Worked Example
Run a query against `documents.docs`, then compare the words in the title, body, tags, and author. The generated `search_vec` column is weighted so title hits outrank body-only hits. The GIN index supports the match predicate, while ranking still has to evaluate candidate rows. ```sql
SELECT id, title, ts_rank_cd(search_vec, websearch_to_tsquery('english', 'postgres indexing')) AS rank
FROM documents.docs
WHERE search_vec @@ websearch_to_tsquery('english', 'postgres indexing')
ORDER BY rank DESC, published_at DESC
LIMIT 10;
```

## Diagnostic Questions
Ask why a row matched, why an expected row did not match, whether the search input was converted safely, whether a category filter belongs before ranking, and whether the plan uses the GIN index for the `@@` predicate. For ranking lessons, ask which field should dominate. For language lessons, ask which configuration created the lexeme and whether accent folding changes user expectations.

## Common Pitfalls
The common mistakes are using `ILIKE '%term%'` as the permanent design for word search, concatenating everything into one unweighted blob, storing a trigger-maintained vector without backfilling old rows, using `to_tsquery` directly on untrusted input, expecting FTS to fix typos, and calling pgvector a replacement for words that must literally appear in documents. Each mistake hides a different requirement and should be repaired by naming that requirement.

## Explain It Back
Explain the search design from evidence: the corpus contains documents, the query asks for words, the vector stores lexemes, the query builder handles user text, the GIN index narrows candidates, ranking orders matches, and snippets help people verify the result. If the requirement changes to typo tolerance, preview `pg_trgm`. If it changes to semantic similarity, point to pgvector in the later extension phase and say not yet until the workload proves it.

## References and Further Reading
Use `docs/search-playbook.md`, `docs/doctrine.md`, and the Phase 7 indexing playbooks. PostgreSQL documentation for text search is the canonical reference for configurations, dictionaries, ranking, and headline behavior. Keep extension choices explicit: `unaccent` is enabled for this phase, `pg_trgm` is only previewed, and pgvector is intentionally deferred.
