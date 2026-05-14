# Plan Debugging Workflow Level B2

## Scenario

A team is debugging a slow containment query and wants a repeatable one-change workflow.

## Task

Compare two candidate access paths or rewrites. Use row estimates, actual rows, buffers, and maintenance cost to decide whether the measured result supports committing the change. Include a before plan, one hypothesis, one measured change, and rollback criteria.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
