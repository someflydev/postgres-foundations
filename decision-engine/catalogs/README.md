# Decision Engine Catalogs

The decision-engine catalogs are JSON-first planning data used by the CLI,
tests, and future rules. Each catalog entry should be explainable from
PostgreSQL behavior, workload signals, operational burden, and portability
constraints.

`industries.json` is the authoritative industry vocabulary for decision
intakes. It connects each industry slug to typical data shapes, workload
patterns, security constraints, tenancy models, scale signals, operational
concerns, failure modes, and internal training references.

`data_shapes.json` is the authoritative catalog for recurring PostgreSQL data
modeling shapes. It maps each shape to core features, relevant extensions,
index patterns, and anti-patterns so the decision engine can explain why a
shape belongs in core PostgreSQL, an extension, or a future stage.

`workload_patterns.json` is the authoritative catalog for runtime behavior and
scale signals. It records thresholds, likely feature implications, topology
implications, and anti-patterns so recommendations are tied to observed
workload pressure rather than generic preference.

`postgres_core_features.json` is the authoritative catalog for PostgreSQL core
and contrib capabilities that should be evaluated before adding operational
surface area. It maps each feature to data shapes, workload patterns, failure
modes, and training references.

`extensions.json` is the authoritative catalog for PostgreSQL extensions and
closely related operational tools. Each entry states when core PostgreSQL is
enough first, then workload fit, operational cost, replication and backup
implications, managed-service availability, adoption triggers, avoidance
triggers, explicit not-yet triggers, prerequisite extensions, extension-track
module slug, and linked anti-patterns.

`index_patterns.json` is the authoritative catalog for recurring index design
patterns. It records the underlying index type, applicable data shapes and
workloads, tradeoffs, and lesson references so recommendations can explain why
an index shape fits a query pattern.

`topology_patterns.json` is the authoritative catalog for deployment and
replication topologies. It captures fit, operational cost, failure modes, and
training references for patterns ranging from a single primary to logical
replication bridges and distributed clusters.

`anti_patterns.json` is the authoritative catalog for common PostgreSQL design
and operations failure modes. Each anti-pattern links to a slug-aligned Markdown
page under `docs/anti-patterns/`, and the catalog checker fails if a referenced
page is missing.
