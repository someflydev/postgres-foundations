# Repair the Finding Duplication on Paper model

## Setup

This is a Phase 0 paper-modeling exercise. Do not write SQL. Work in markdown.

## Given

A migration team imports legacy customers and orders in batches. Legacy identifiers are not globally unique, and several source rows may refer to the same real customer. Reviewers need to trace which import batch produced each mapping decision.

The flawed model says: legacy customer number is globally unique; import batch date is copied onto every mapped customer; one free-text note stores all mapping reasons; legacy orders are not related to import batches; corrections overwrite the original mapping decision.

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
