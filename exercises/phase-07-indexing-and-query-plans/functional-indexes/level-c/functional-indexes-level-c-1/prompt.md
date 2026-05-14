# Functional Indexes Level C1

## Scenario

Support needs case-insensitive customer email lookup and daily order buckets.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend whether the expression index or a clearer modeled value should win with an expression index that exactly matches lower(email) or date_trunc usage.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
