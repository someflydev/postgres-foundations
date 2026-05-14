# BRIN for Append Heavy Chronological Data Level D2

## Scenario

An append-heavy events table is filtered by occurred_at windows during investigations.

## Task

Critique the proposed fix. Name the broken assumption, capture or describe the plan evidence, and defend whether BRIN is enough or the workload needs B-tree, partitioning, or retention work. Your answer must include the artifact: a BRIN index justified by physical correlation between heap order and occurred_at.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
