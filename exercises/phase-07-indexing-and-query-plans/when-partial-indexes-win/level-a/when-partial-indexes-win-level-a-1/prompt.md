# When Partial Indexes Win Level A1

## Scenario

The operations dashboard reads rare pending orders ordered by recent placement time.

## Task

Identify the predicate, expression, or operator that drives the plan. Record the baseline evidence and explain what a partial index whose predicate is provably implied by the query would prove before deciding the pending-order dashboard should keep or reject the partial index.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
