# BRIN for Append Heavy Chronological Data Level A1

## Scenario

An append-heavy events table is filtered by occurred_at windows during investigations.

## Task

Identify the predicate, expression, or operator that drives the plan. Record the baseline evidence and explain what a BRIN index justified by physical correlation between heap order and occurred_at would prove before deciding whether BRIN is enough or the workload needs B-tree, partitioning, or retention work.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
