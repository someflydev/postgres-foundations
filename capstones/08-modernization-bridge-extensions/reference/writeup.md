# Modernization Bridge Extensions Reference Writeup

## Modeling

The new service owns accounts, orders, search fields, and BI aggregates. Legacy identifiers are references, not the primary source for new writes. Materialized views expose stable aggregates to BI without putting dashboard load on transactional joins.

## FDW

postgres_fdw is used for selective reads from the legacy system. The runbook requires EXPLAIN on both sides because a query that looks selective locally may still fetch too many remote rows if pushdown fails. Async append is useful when independent foreign scans can run concurrently, but it is not a substitute for good predicates.

## Indexes

Core FTS handles explainable search across account names and notes. pg_trgm handles misspellings and partial-name searches. Materialized views get unique indexes so refresh and BI reads have a stable access path.

## Operations

pg_stat_statements must be enabled on both databases. The new service tracks local search, materialized view refresh, and FDW query time. The legacy side tracks whether bridge reads are creating load that legacy owners did not approve.

## Extension posture

postgres_fdw is now because the modernization bridge must read legacy rows without copying the whole monolith on day one. It is a narrow dependency with clear operational concerns: credentials, pushdown, remote load, network latency, and failure isolation. The design uses foreign tables for read paths and local tables for new writes so the bridge can progress incrementally.

Core FTS and pg_trgm are now because the new service needs search and typo tolerance over local records. These features are portable, explainable, and sufficient for account and notes search. pgvector is avoid for now because the search requirement is lexical and fuzzy, not conceptual.

Logical replication to the BI replica is now or near-now depending on reporting load. The reference posture configures it as the read-isolation path for aggregates, with slot lag and publication drift in the runbook. It should not replace transactional correctness in the new service.

Citus is avoid for now. The team member's proposal lacks a distribution key that improves the dominant workload. Tenant_id is a possible distribution key, but the bridge still needs cross-tenant BI aggregates, legacy identity reconciliation, and FDW reads that would not become simpler when sharded. Account_id would distribute orders but would make tenant-level reporting and account search less coherent. The progression trigger is concrete: single-node PostgreSQL must show sustained CPU, memory, or IO saturation after indexes, materialized views, and replica isolation are correct, and the team must prove that tenant_id keeps joins and writes shard-local. Until then Citus adds planning, migration, operations, and managed-service constraints without solving the current problem.

## Not yet

Do not enable Citus or semantic search now. Promote only when measured workload limits and a defensible distribution key exist. Keep FDW reads selective and make the BI replica absorb reporting pressure before reaching for distributed PostgreSQL.

## Detailed defense

The modernization bridge succeeds only if it is honest about ownership. The new service owns its local account and order model. The legacy system remains the source for legacy customer and invoice facts until migration work moves those facts. FDW is a bridge for selective reads, not an excuse to build a hidden distributed monolith. The schema records legacy identifiers so the service can reconcile old and new records while keeping new writes local and auditable.

The account table includes tenant_id because the new service needs an explicit access boundary. It includes legacy_customer_id as a nullable reference because not every new account may have a legacy counterpart and not every legacy customer may be migrated immediately. This avoids a false assumption that modernization is a single cutover. Orders belong to local accounts and are not written back through FDW. That is intentional. Writing across a fragile bridge would couple the new service's correctness to legacy availability.

Search is local because the new service needs to search the records it owns. Core full-text search handles account names and notes with explainable ranking. pg_trgm handles misspellings and partial names, which are common in support and account-management workflows. This search posture is narrower than the AI knowledge platform. There is no semantic discovery requirement, no embedding pipeline, and no model owner. FTS and pg_trgm solve the stated problem with much lower operational burden.

The materialized BI view is also local. It gives reporting a stable aggregate shape and avoids making BI tools join transactional tables repeatedly. The unique index on the materialized view provides a stable access path and supports concurrent refresh in environments where the refresh mode is used. The view has a freshness contract: it is correct as of the last refresh, not as of the current transaction. That difference should be visible to BI users and operators.

postgres_fdw is a now decision because the new service must read selected legacy data while the migration is incomplete. The important word is selected. The FDW path should use predicates that can be pushed down, should import only the needed foreign tables or views, and should avoid broad joins that move large legacy row sets into the new database. A bridge query that fetches millions of remote rows is a design failure, not an FDW limitation.

Pushdown verification is mandatory. Operators need to inspect EXPLAIN output and confirm that filters, projections, and compatible joins run remotely when expected. The new database's planner estimates may not match legacy reality. The runbook should include examples of good and bad plans, including signs that a remote scan is returning too many rows. When pushdown is not possible, the team should either narrow the query, add a legacy-side view, or copy a small reference subset intentionally.

Async append is useful but easy to overstate. It can help when independent foreign scans can proceed concurrently, especially across partition-like foreign tables or separate remote sources. It does not fix poor selectivity, missing remote indexes, or a network path that is the bottleneck. The writeup should treat async append as an optimization to verify, not as the reason FDW is safe.

pg_stat_statements on both sides is central. The new service can see local query cost and normalized FDW statements. The legacy database can see the actual remote workload imposed by the bridge user. Both views are needed because the new team and legacy owners may experience different symptoms. A query may look cheap locally because it returns few rows but still be expensive remotely because the legacy side scanned a large table before applying a filter.

The FDW security posture should be narrow. The bridge user should have read-only access to approved legacy objects. User mappings should not grant broad superuser-like access. If legacy data includes sensitive fields, expose a legacy view that omits them rather than importing whole tables and trusting every local query. The new service's RLS policies protect local tenant-owned rows, but they do not automatically protect legacy tables. That distinction must be clear in the writeup.

Logical replication to BI is a read-isolation strategy, not the migration mechanism for every path. The BI replica can subscribe to publications from the new service so reporting tools do not compete with transactional traffic. The team must monitor replication slots, lag, schema changes, and subscriber health. If the subscriber stalls, WAL retention on the publisher can become an incident. That operational cost is acceptable when BI load is real and freshness expectations are documented.

A logical replication configuration artifact should state what is published, why it is published, and what is excluded. Publishing every table by default is convenient but risky. The reference posture should prefer a publication for BI-facing tables or materialized outputs where possible. If BI needs raw transactional tables, the schema-change process must include subscriber compatibility checks. The operational runbook should name who owns broken subscriptions after migrations.

Citus is the judgment challenge. It is tempting to adopt it because modernization projects often talk about future scale, but scale as a slogan is not a workload signal. A distributed database needs a distribution key, co-location strategy, backup and restore plan, and operational ownership. The bridge workload has local writes, local search, FDW reads, and BI aggregates. None of those automatically becomes better when sharded.

Tenant_id is the most plausible distribution key. It could make tenant-local account and order queries shard-local. However, the bridge also needs cross-tenant BI aggregates, account search, legacy reconciliation, and administrative views. If tenant_id is used too early, the team may discover that many operational queries are cross-shard. Account_id is another possible key, but it weakens tenant-level reporting and does not align with tenant-scoped RLS as cleanly. Legacy_customer_id is worse because new records may not have one and legacy identifiers should not control the new service's physical layout.

The correct Citus decision is avoid for now. The system has not proven that single-node PostgreSQL with proper indexes, materialized views, FDW discipline, and a BI replica is insufficient. It has not proven a distribution key. It has not shown that the operations team is ready for distributed query planning, shard rebalancing, distributed backups, or version-specific managed-service constraints. Avoiding Citus now is not rejecting it forever. It is requiring evidence before accepting its burden.

The progression trigger for Citus should be measurable. The team should first exhaust ordinary PostgreSQL: inspect pg_stat_statements, tune indexes, move BI load to the replica, refresh aggregates appropriately, and constrain FDW queries. If the primary still has sustained CPU, memory, IO, or storage pressure from tenant-local workloads, and if analysis shows tenant_id keeps dominant joins and writes local, then Citus can become a candidate. The proposal should include expected cross-shard queries and their acceptable latency.

Search should also resist premature semantic expansion. The local search problem is account names and operational notes. FTS and pg_trgm are enough. pgvector would add embeddings, model changes, index rebuilds, and relevance testing without a conceptual retrieval use case. If account managers later need "find customers similar to this churn pattern", that is an analytics or ML requirement with separate data preparation. It should not be smuggled into the bridge search path.

Materialized views need refresh discipline. Refreshing too often can compete with writes. Refreshing too rarely can make BI decisions stale. The view should expose or be paired with a freshness timestamp in a production design. BI users should know whether they are looking at data from five minutes ago or last night. If concurrent refresh is used, the unique index requirement must be maintained. If refresh cost grows, the next step might be incremental summary tables rather than a new extension.

The bridge also needs migration posture. FDW reads can help compare local and legacy facts, but long-term modernization should reduce runtime dependency on the legacy database. The team should track which workflows still require legacy reads, which data has been copied or re-owned, and which foreign tables can be retired. A bridge with no retirement plan becomes permanent coupling. The writeup should include triggers for replacing FDW reads with local ownership or logical replication paths.

Failure modes should be explicit. If the legacy database is down, local writes should continue where they do not require legacy confirmation. FDW-dependent screens should fail clearly and avoid retry storms. If BI replication lags, transactional behavior should continue while dashboards show lag. If search indexes bloat, account writes should not be blocked by emergency reindexing without a plan. These are design requirements, not operational afterthoughts.

Portability is mixed but manageable. postgres_fdw, FTS, and pg_trgm are standard PostgreSQL capabilities or common extensions. Logical replication is core PostgreSQL. Citus is the portability boundary that the reference refuses to cross without evidence. That makes the first design suitable for a broad range of managed PostgreSQL environments. The team should still test provider-specific FDW, replication, and extension support because managed services differ in permissions and networking.

The final architecture is intentionally incremental. It gives the new service local truth, local search, controlled legacy reads, BI isolation, and a written path for extension decisions. It rejects Citus and pgvector because the current workload does not justify their operational costs. It adopts postgres_fdw, FTS, pg_trgm, and logical replication posture because those map directly to current requirements. That is the modernization version of core-first extension discipline.

## Reviewer checklist

A reviewer should start by checking ownership boundaries. Local tables should own new-service truth. Foreign tables should support selective legacy reads. If the design writes through FDW into the legacy system or makes every local request depend on broad remote joins, the bridge is too tightly coupled. Modernization should reduce legacy dependency over time, not hide it behind SQL.

The second review point is pushdown evidence. A good answer explains how the team verifies remote filters and joins, what happens when pushdown fails, and how legacy-side pg_stat_statements is reviewed. FDW without remote observability can harm the legacy system while looking harmless from the new service.

The third review point is search scope. FTS and pg_trgm fit local account and note search. pgvector does not belong unless there is a conceptual retrieval workflow with an embedding owner. The learner should not import the AI knowledge-platform solution into a bridge capstone without evidence.

The fourth review point is BI isolation. Logical replication and materialized views should have freshness, lag, and schema-change posture. A report that is five minutes stale may be acceptable; a report with unknown lag is not. The learner should name publications, subscribers, slot monitoring, and failure handling.

The final review point is Citus. Any adoption must include a distribution key, co-location reasoning, cross-shard query analysis, and a proof that single-node PostgreSQL plus indexes, materialized views, replica isolation, and selective FDW reads is insufficient. If the answer merely says "Citus for scale", it should trigger the posture signal and require revision.

Reviewers should also ask how the bridge is retired. Each FDW dependency should have an owner and a target state: keep as read-through, copy into local ownership, replace with logical replication, or remove after the legacy workflow is migrated. Without that inventory, a bridge becomes permanent infrastructure with unclear accountability. The reference design is acceptable because it makes local truth explicit and treats FDW as a controlled integration surface.

Finally, the learner should describe change coordination. Legacy schema changes can break foreign tables. New-service schema changes can break BI subscribers. Search-index changes can alter support workflows. A good runbook names compatibility checks, staging validation, and communication with legacy and BI owners. Modernization is as much organizational sequencing as SQL design, and the extension posture should reflect that coordination cost.

The bridge should be evaluated with rollback scenarios. If an FDW query becomes slow, the team can disable the affected feature or route it to a cached view. If BI replication lags, transactional writes continue while reports show stale status. If a Citus proposal returns later, it should arrive with measurements, not urgency. Those rollback stories prove the design is incremental rather than a risky rewrite hidden behind extensions.

Reviewers should also check for naming discipline. Legacy identifiers, local identifiers, and BI-facing identifiers should be clearly distinct. Ambiguous names make reconciliation errors harder to find and can cause teams to mistake a legacy reference for local ownership.
