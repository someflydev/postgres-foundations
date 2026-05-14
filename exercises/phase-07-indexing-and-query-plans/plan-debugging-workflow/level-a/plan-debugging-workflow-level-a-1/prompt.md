# Plan Debugging Workflow Level A1

## Scenario

A team is debugging a slow containment query and wants a repeatable one-change workflow.

## Task

Identify the predicate, expression, or operator that drives the plan. Record the baseline evidence and explain what a before plan, one hypothesis, one measured change, and rollback criteria would prove before deciding whether the measured result supports committing the change.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
