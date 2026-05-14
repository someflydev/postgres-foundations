# EXPLAIN ANALYZE Deep Dive Level C1

## Scenario

A tenant-and-status query has a severe estimated rows versus actual rows mismatch.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend whether the next change should be ANALYZE, extended statistics, a query rewrite, or an index with plan evidence from rows, loops, buffers, and CREATE STATISTICS before adding another index.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
