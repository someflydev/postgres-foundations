# When Partial Indexes Win Level B2

## Scenario

The operations dashboard reads rare pending orders ordered by recent placement time.

## Task

Compare two candidate access paths or rewrites. Use row estimates, actual rows, buffers, and maintenance cost to decide the pending-order dashboard should keep or reject the partial index. Include a partial index whose predicate is provably implied by the query.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
