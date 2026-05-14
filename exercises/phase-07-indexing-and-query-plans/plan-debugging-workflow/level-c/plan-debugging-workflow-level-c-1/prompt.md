# Plan Debugging Workflow Level C1

## Scenario

A team is debugging a slow containment query and wants a repeatable one-change workflow.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend whether the measured result supports committing the change with a before plan, one hypothesis, one measured change, and rollback criteria.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
