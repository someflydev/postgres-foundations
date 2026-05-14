# Functional Indexes Level B1

## Scenario

Support needs case-insensitive customer email lookup and daily order buckets.

## Task

Compare two candidate access paths or rewrites. Use row estimates, actual rows, buffers, and maintenance cost to decide whether the expression index or a clearer modeled value should win. Include an expression index that exactly matches lower(email) or date_trunc usage.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
