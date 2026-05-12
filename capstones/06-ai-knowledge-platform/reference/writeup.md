# AI Knowledge Platform Reference Writeup

## Modeling

Documents store source, title, body, team scope, and a generated search vector. Chunks store embedding text boundaries, model identity, and pgvector vectors. This keeps document metadata relational and lets embeddings be rebuilt without overwriting the canonical document.

## Indexes

Core FTS uses GIN over the generated tsvector. Typo tolerance uses pg_trgm over titles and can be extended to selected fields. Semantic retrieval uses pgvector HNSW with cosine distance. The indexes serve different query classes and should be observed separately.

## Hybrid ranking

Hybrid retrieval uses reciprocal rank fusion. Lexical and semantic subqueries produce ranked document IDs. The final query sums `1 / (60 + rank)` across result sets, which rewards documents that appear in both channels while still allowing a strong single channel to surface.

## Operations

Operators inspect pg_stat_statements by query family. Embedding model changes are handled as a parallel write path: generate embeddings with a new model name, build replacement indexes, compare quality, switch traffic, and retire old vectors after rollback is no longer needed.

## Extension posture

Core full-text search is a now decision because engineers often know exact service names, errors, runbook titles, and operational terms. FTS gives explainable ranking, works in plain PostgreSQL, and remains the fallback when semantic retrieval is unavailable. pg_trgm is also now because typo tolerance is a stated use case and the extension is small, mature, and available in common managed PostgreSQL services.

pgvector is now, but only after the lexical baseline is kept. The use case explicitly includes conceptual discovery, such as finding documents related to an architectural idea even when exact words differ. That is the workload signal FTS and pg_trgm cannot fully satisfy. The operational burden is real: embedding generation, model versioning, HNSW memory, rebuild windows, and quality evaluation need owners. The design isolates that burden in `document_chunks` so documents remain queryable through lexical search during vector incidents.

TimescaleDB is avoid for now. The system has document growth, not high-frequency time-series ingest, retention automation, or downsampling needs. Citus is avoid for now because 80,000 documents plus weekly growth do not justify distributed PostgreSQL, and there is no distribution key that improves the primary retrieval path without adding cross-shard ranking complexity.

The portability posture is managed-service first. The target is AWS RDS or another provider with pgvector available. If a provider lacks HNSW, the fallback is exact vector search at smaller limits while lexical search remains the production baseline. The trigger to revisit the design is measured retrieval latency or quality loss after realistic corpus growth, not the mere existence of AI features.

## Not yet

Do not add TimescaleDB, Citus, or a separate search cluster until pg_stat_statements, quality review, and corpus growth show PostgreSQL cannot meet the stated retrieval goals.

## Detailed defense

The knowledge platform has three different retrieval problems, and the design keeps them separate before combining them. Lexical search answers questions where the user knows words from the document: service names, error strings, runbook titles, API names, and incident labels. Fuzzy search answers questions where the user nearly knows the words but misspells them or remembers only part of a title. Semantic search answers questions where the user knows the concept but not the vocabulary. Hybrid search exists because real engineering questions often combine all three.

The document table remains the canonical source of metadata and body text. It stores source system, team scope, title, body, update time, and a generated search vector. This keeps ordinary PostgreSQL constraints and backup behavior around the most important data. The chunk table stores derived retrieval units and embeddings. Chunks are separate because embedding generation is a pipeline with its own failure modes, latency, model versions, and quality checks. Rebuilding embeddings should not rewrite the canonical document row unless the source document changed.

The generated tsvector gives the system an explainable baseline. Titles are weighted higher than body text because a title match is usually more meaningful for documentation discovery. The exact weighting can change, but it should be measured against search-quality examples rather than tuned by taste. FTS also provides a dependable fallback when vector search is degraded, unavailable, or under rebuild. A knowledge-search platform that cannot answer exact keyword searches during an embedding incident is not operationally mature.

pg_trgm is justified by the typo-tolerance requirement. Engineers often search for service names, internal tools, acronyms, and project names from memory. Trigram matching over titles gives a cheap way to catch misspellings and partial names. It should not be sprayed across every large text field by default. Applying trigram indexes to full body text can create heavy write and storage cost. The first design indexes titles, then expands only when pg_stat_statements and search logs show fuzzy body search is needed.

pgvector is justified because the prompt includes conceptual discovery as a first-class use case. "Find docs conceptually related to this design" cannot be solved reliably with only FTS or trigrams when the relevant documents use different vocabulary. The writeup must still compare pgvector to the lexical baseline, because semantic search is not a replacement for exact search. It is a complementary retrieval channel with more operational burden. The reference design keeps that burden in `document_chunks`, where each row records the embedding model used to produce the vector.

HNSW is the right reference index because the corpus is large enough that exact vector search may become expensive, and the use case expects interactive retrieval. The index choice should come with ownership notes. HNSW uses memory and has build-time cost. It also represents vectors for a specific embedding model. When the model changes, the old index should not be reused as if vectors were comparable. The correct approach is parallel embeddings with a new model identifier, a new or rebuilt index, quality comparison, and a controlled switch.

Hybrid retrieval uses reciprocal rank fusion because it is simple, inspectable, and robust when component scores are not directly comparable. FTS rank, trigram similarity, and vector distance live on different scales. RRF turns each channel into ranks and rewards documents that appear near the top in more than one channel. The constant, such as 60, should be treated as a tuning parameter tested against sample queries. The system can later add channel weights, but the first version should prove the simpler fusion scheme.

Access control is modeled by team scope in the document table. In a real deployment, the visibility model may need document-level ACLs, group memberships, or source-system permissions. The reference stays intentionally small but shows the expected posture: search queries should filter by visibility before returning results. Vector retrieval needs particular care because retrieving chunk IDs before applying authorization can leak titles or snippets through timing, ranking, or logs. Production hybrid queries must enforce access consistently across lexical and semantic paths.

The managed-service requirement shapes every extension decision. Core FTS and pg_trgm are widely available in managed PostgreSQL. pgvector is increasingly available but still needs provider confirmation, version checks, and index capability checks. TimescaleDB and Citus are excluded because they solve different problems and are not necessary for an 80,000-document internal corpus with weekly growth. A separate search service is also not the first move because the prompt asks for a PostgreSQL-first design and the stated scale is well within a careful relational implementation.

The ingestion pipeline should be explicit even though the capstone focuses on database artifacts. Documents arrive from source systems, are normalized into canonical rows, are chunked, and then embeddings are generated. Each stage should be idempotent. If embedding generation fails, the document should still be searchable through FTS and pg_trgm. If a source document is deleted or access scope changes, derived chunks must follow. The schema uses `ON DELETE CASCADE` for chunks to keep derived data from outliving the document row.

Search quality cannot be judged only by latency. The team needs a small evaluation set of real engineering questions with expected useful documents. Lexical-only, semantic-only, and hybrid results should be compared regularly. The runbook should include relevance regressions after model changes, not just query failures. A new embedding model that is faster but misses critical runbooks is not an improvement. A hybrid ranking change that promotes popular but irrelevant docs should be caught before it reaches production.

pg_stat_statements is still useful in a search product. It can show whether FTS queries dominate total time, whether vector queries have high mean latency, whether fuzzy title searches are being called excessively by autocomplete, and whether hybrid queries are doing too much work before limiting candidates. Search logs can explain quality; pg_stat_statements explains database cost. Both are needed before adding indexes or changing ranking.

The operational response to slow lexical search is different from slow semantic search. Slow FTS might need query normalization, better dictionaries, generated vectors, or narrower filters. Slow trigram search might need tighter similarity thresholds or a narrower indexed column set. Slow vector search might need a better candidate limit, HNSW parameter review, more memory, or exact-search fallback for small filtered sets. Treating all search latency as the same problem leads to cargo-culted indexing.

Embedding model changes are the most important lifecycle event. The system must not overwrite vectors in place without a comparison window. A model change can alter vector dimensions, distance distribution, and semantic neighborhoods. The reference design stores `embedding_model` and makes it part of chunk uniqueness. A migration can write new vectors beside old ones, build a matching HNSW index, run offline quality checks, then switch read queries by model. After the rollback window closes, old vectors can be removed.

Reindex posture is tied to the data type. GIN indexes for FTS and trigram may need maintenance after large ingestion bursts or delete churn, but they are not rebuilt because a semantic model changed. HNSW indexes represent a specific vector population and should be rebuilt when that population is replaced. The runbook should name these differences so an incident response does not rebuild every index blindly. Reindexing is an operational intervention with lock, IO, and scheduling consequences.

The design should be careful with snippets and result presentation. The database can return document IDs, titles, ranks, and chunk IDs. The application can render highlighted snippets and enforce source-specific links. If snippets are generated in SQL, they should be bounded and tested for latency. The capstone's database responsibility is retrieval correctness and ranking evidence, not a full product UI.

TimescaleDB is avoid for now because the system is not a time-series workload. Document update time exists, but the critical queries are search queries, not time-bucket analytics, retention policies, or high-frequency measurements. Adding TimescaleDB would create an extension dependency without improving lexical, fuzzy, semantic, or hybrid retrieval. If later the platform collects high-volume search telemetry, that telemetry can be modeled separately and evaluated on its own merits.

Citus is avoid for now because distribution would complicate ranking. Search wants global top-N results across the visible corpus. Sharding by team might help authorization locality but would make cross-team platform searches and global ranking harder. Sharding by document ID would not help team-scoped queries. At 80,000 documents with weekly growth, single-node PostgreSQL plus appropriate indexes is the right baseline. The trigger for revisiting Citus would be measured single-node limits and a distribution key that keeps dominant queries shard-local.

The portability fallback matters. If a provider supports pgvector but not HNSW, the team can run exact vector search over narrowed candidate sets or rely more heavily on lexical search while evaluating provider options. If pgvector is unavailable entirely, the system still has a useful product with FTS and pg_trgm. That is why the lexical baseline is not optional. It is the operational fallback and the quality comparison point.

The final posture is a balanced one. Use PostgreSQL core for exact document retrieval. Use pg_trgm for a narrow fuzzy requirement. Use pgvector for the explicit semantic requirement, but isolate it as derived data with model versioning and rebuild discipline. Reject time-series and distributed extensions until workload evidence demands them. The result is an AI-aware design that remains understandable to database operators and reviewable by human architects.

## Reviewer checklist

A reviewer should start by looking for a lexical baseline. If the answer enables pgvector but does not show FTS and pg_trgm queries, it has skipped the most reliable and explainable search paths. Semantic retrieval should be accepted because the use case asks for conceptual discovery, not because "AI" appears in the system name. The writeup should say which queries lexical search handles better and which queries embeddings handle better.

The second review point is derived-data lifecycle. Embeddings are not canonical facts. They are generated artifacts tied to a chunking strategy and model version. A strong design stores model identity, supports parallel rebuilds, and explains how old vectors are retired. A weak design overwrites vectors in place and gives no rollback path when quality drops.

The third review point is hybrid ranking. The learner should not simply union lexical and vector results without explaining score comparability. RRF is acceptable because it fuses ranks rather than pretending FTS rank and cosine distance share a scale. If the learner proposes a different fusion method, ask for the calibration and quality-evaluation plan.

The fourth review point is authorization. Search systems are prone to accidental leakage because retrieval and rendering are often separated. A good answer applies visibility filters consistently before results are exposed, including semantic chunk retrieval. If vector search retrieves unauthorized chunks and filters later, the learner should explain why no titles, snippets, timing, or logs leak sensitive information.

The final review point is portability. The capstone requires managed PostgreSQL with pgvector assumed available, not a specialized search platform. A good solution names what happens if HNSW support differs by provider, how FTS keeps the system useful during vector outages, and why TimescaleDB and Citus do not improve this document-retrieval workload.

The learner should also explain how results are observed after launch. Search logs should capture query text, selected channel, clicked document, empty-result cases, and latency without storing sensitive document content unnecessarily. Those logs help distinguish a ranking problem from a corpus problem. If users cannot find a document because it was never ingested, adding another index will not help. If users search with exact terms and get poor results, FTS configuration is the first suspect. If conceptual questions fail while lexical queries succeed, the embedding model, chunking strategy, or hybrid fusion should be reviewed.

Finally, reviewers should expect a model-governance note. Even an internal platform can expose confidential engineering plans, incident details, or customer-sensitive data. The embedding process should run in an approved environment, should respect document access scope, and should have a deletion path when source documents are removed. The database design cannot solve every governance concern, but it should make derived vectors traceable to source documents and model versions so operations and security teams can reason about them.

The submission is strongest when it includes a small failure-mode table in prose: lexical index unavailable, vector index rebuilding, embedding worker delayed, source connector stale, and access-scope change pending. For each case, the learner should say what still works, what is degraded, and which operator signal proves recovery. That habit keeps the platform from becoming a demo that works only on a happy path.
