# Functional Indexes Level A2

## Scenario

Support needs case-insensitive customer email lookup and daily order buckets.

## Task

Identify the predicate, expression, or operator that drives the plan. Record the baseline evidence and explain what an expression index that exactly matches lower(email) or date_trunc usage would prove before deciding whether the expression index or a clearer modeled value should win.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
