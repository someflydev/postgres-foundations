# Build the Identity Without IDs model

## Setup

This is a Phase 0 paper-modeling exercise. Do not write SQL. Work in markdown.

## Given

A migration team imports legacy customers and orders in batches. Legacy identifiers are not globally unique, and several source rows may refer to the same real customer. Reviewers need to trace which import batch produced each mapping decision.

## Task

Produce the full paper model with entities, attributes, relationships, invariants, lifecycle events, and unresolved questions. Note that this uses the modeling variant of the paper-modeling rubric.

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

- Produces entities, attributes, relationships, invariants, and lifecycle events without scaffolding.
- Explains cardinality for each relationship.
- Answers both oral-defense prompts from the model.

## Oral Defense

- Which of these invariants cannot be expressed in a table and why?
- Which lifecycle events produce new rows vs update rows?
## Estimated Time

35 minutes.
