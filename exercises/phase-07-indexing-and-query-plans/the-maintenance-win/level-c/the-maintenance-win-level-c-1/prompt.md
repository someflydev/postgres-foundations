# The Maintenance Win Level C1

## Scenario

An orders table has overlapping customer and status indexes from several tuning passes.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend which index should be kept, replaced, or dropped concurrently with unused or redundant index maintenance cost using size and scan evidence.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
