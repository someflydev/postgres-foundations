# Functional Indexes Level D1

## Scenario

Support needs case-insensitive customer email lookup and daily order buckets.

## Task

Critique the proposed fix. Name the broken assumption, capture or describe the plan evidence, and defend whether the expression index or a clearer modeled value should win. Your answer must include the artifact: an expression index that exactly matches lower(email) or date_trunc usage.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
