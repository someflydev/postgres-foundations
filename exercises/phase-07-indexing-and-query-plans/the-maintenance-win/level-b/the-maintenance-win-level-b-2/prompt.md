# The Maintenance Win Level B2

## Scenario

An orders table has overlapping customer and status indexes from several tuning passes.

## Task

Compare two candidate access paths or rewrites. Use row estimates, actual rows, buffers, and maintenance cost to decide which index should be kept, replaced, or dropped concurrently. Include unused or redundant index maintenance cost using size and scan evidence.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
