# GIN Cost Model Level A2

## Scenario

A write-heavy event table proposes a broad GIN index on frequently updated payloads.

## Task

Identify the predicate, expression, or operator that drives the plan. Record the baseline evidence and explain what GIN read value against fastupdate, pending list, bloat, and write amplification would prove before deciding whether the GIN index is worth keeping or should be narrowed, redesigned, or deferred.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
