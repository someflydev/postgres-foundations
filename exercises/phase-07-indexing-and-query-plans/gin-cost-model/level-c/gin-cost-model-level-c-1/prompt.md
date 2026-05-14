# GIN Cost Model Level C1

## Scenario

A write-heavy event table proposes a broad GIN index on frequently updated payloads.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend whether the GIN index is worth keeping or should be narrowed, redesigned, or deferred with GIN read value against fastupdate, pending list, bloat, and write amplification.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
