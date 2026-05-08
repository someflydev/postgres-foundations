# Repair the Invariants Before Enforcement model

## Setup

This is a Phase 0 paper-modeling exercise. Do not write SQL. Work in markdown.

## Given

A store tracks customers who place orders. Each order has a current status, order date, and one or more product lines. Product names and current catalog prices can change after an order is placed, but the team still needs to explain what the customer bought at the time.

The flawed model says: customer email is copied into every order and order item; product name is the only product identity; order status can be any phrase; line items have no relationship to orders; refunds overwrite the original placed event.

## Task

Diagnose and repair the flawed paper model. Find at least three concrete flaws involving duplication, missing relationships, weak invariants, or lifecycle confusion. Note that this uses the modeling variant of the paper-modeling rubric.

## Allowed Concepts

- entity
- attribute
- relationship
- cardinality
- identity
- duplication
- invariant
- lifecycle-event
- state-transition

## Not Yet Allowed

- select
- insert
- foreign_key
- primary_key
- normalization
- join
- index
- transaction
- constraint

## Success Criteria

- Identifies at least three concrete flaws in the flawed model.
- Repairs the model while preserving the stated business facts.
- Justifies each repair during oral defense.

## Oral Defense

- Justify the repair for each duplicated fact.
- Which missing relationship caused the largest loss of meaning?
- Which lifecycle event or invariant prevents the repaired model from drifting again?
## Estimated Time

45 minutes.
