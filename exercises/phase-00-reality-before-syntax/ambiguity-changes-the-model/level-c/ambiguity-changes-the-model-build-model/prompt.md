# Build the Ambiguity Changes the Model model

## Setup

This is a Phase 0 paper-modeling exercise. Do not write SQL. Work in markdown.

## Given

An operations system receives events from many sources. Events have source-local identifiers, types, timestamps, and current triage state. Some events become linked to incidents, and operators need history for classification and resolution changes.

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
