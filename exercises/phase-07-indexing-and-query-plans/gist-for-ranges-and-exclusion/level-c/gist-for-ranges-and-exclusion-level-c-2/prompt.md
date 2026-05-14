# GiST for Ranges and Exclusion Level C2

## Scenario

Scheduling needs to find and prevent overlapping provider appointment windows.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend whether the requirement is read performance, write-time correctness, or both with a GiST-backed range overlap query or exclusion constraint using the && operator.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
