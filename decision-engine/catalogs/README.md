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
