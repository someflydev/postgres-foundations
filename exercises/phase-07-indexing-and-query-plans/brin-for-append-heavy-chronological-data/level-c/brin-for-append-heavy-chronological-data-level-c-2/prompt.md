# BRIN for Append Heavy Chronological Data Level C2

## Scenario

An append-heavy events table is filtered by occurred_at windows during investigations.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend whether BRIN is enough or the workload needs B-tree, partitioning, or retention work with a BRIN index justified by physical correlation between heap order and occurred_at.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
