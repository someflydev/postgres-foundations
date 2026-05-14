# When Partial Indexes Win Level C1

## Scenario

The operations dashboard reads rare pending orders ordered by recent placement time.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend the pending-order dashboard should keep or reject the partial index with a partial index whose predicate is provably implied by the query.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
