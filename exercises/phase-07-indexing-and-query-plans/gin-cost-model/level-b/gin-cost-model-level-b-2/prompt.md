# GIN Cost Model Level B2

## Scenario

A write-heavy event table proposes a broad GIN index on frequently updated payloads.

## Task

Compare two candidate access paths or rewrites. Use row estimates, actual rows, buffers, and maintenance cost to decide whether the GIN index is worth keeping or should be narrowed, redesigned, or deferred. Include GIN read value against fastupdate, pending list, bloat, and write amplification.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
