# GIN Cost Model Level D1

## Scenario

A write-heavy event table proposes a broad GIN index on frequently updated payloads.

## Task

Critique the proposed fix. Name the broken assumption, capture or describe the plan evidence, and defend whether the GIN index is worth keeping or should be narrowed, redesigned, or deferred. Your answer must include the artifact: GIN read value against fastupdate, pending list, bloat, and write amplification.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
