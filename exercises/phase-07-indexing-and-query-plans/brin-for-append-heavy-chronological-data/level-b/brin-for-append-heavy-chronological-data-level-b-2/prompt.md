# BRIN for Append Heavy Chronological Data Level B2

## Scenario

An append-heavy events table is filtered by occurred_at windows during investigations.

## Task

Compare two candidate access paths or rewrites. Use row estimates, actual rows, buffers, and maintenance cost to decide whether BRIN is enough or the workload needs B-tree, partitioning, or retention work. Include a BRIN index justified by physical correlation between heap order and occurred_at.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
