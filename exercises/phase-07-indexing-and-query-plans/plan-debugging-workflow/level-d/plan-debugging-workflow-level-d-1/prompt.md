# Plan Debugging Workflow Level D1

## Scenario

A team is debugging a slow containment query and wants a repeatable one-change workflow.

## Task

Critique the proposed fix. Name the broken assumption, capture or describe the plan evidence, and defend whether the measured result supports committing the change. Your answer must include the artifact: a before plan, one hypothesis, one measured change, and rollback criteria.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.
