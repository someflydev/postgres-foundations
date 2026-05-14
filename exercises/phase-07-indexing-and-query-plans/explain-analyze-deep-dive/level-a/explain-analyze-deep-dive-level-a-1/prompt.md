# EXPLAIN ANALYZE Deep Dive Level A1

## Scenario

A tenant-and-status query has a severe estimated rows versus actual rows mismatch.

## Task

Identify the predicate, expression, or operator that drives the plan. Record the baseline evidence and explain what plan evidence from rows, loops, buffers, and CREATE STATISTICS before adding another index would prove before deciding whether the next change should be ANALYZE, extended statistics, a query rewrite, or an index.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
