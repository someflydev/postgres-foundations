# EXPLAIN ANALYZE Deep Dive Level D2

## Scenario

A tenant-and-status query has a severe estimated rows versus actual rows mismatch.

## Task

Critique the proposed fix. Name the broken assumption, capture or describe the plan evidence, and defend whether the next change should be ANALYZE, extended statistics, a query rewrite, or an index. Your answer must include the artifact: plan evidence from rows, loops, buffers, and CREATE STATISTICS before adding another index.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
