# GIN for JSONB and Arrays Level C1

## Scenario

Incident responders filter event payloads with JSONB containment and product tags with array membership.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend whether GIN is indexing a sound attribute design or hiding weak modeling with a GIN operator class that matches the actual JSONB or array operator.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
