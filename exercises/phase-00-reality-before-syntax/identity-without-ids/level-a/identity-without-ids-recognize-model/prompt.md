# Recognize the Identity Without IDs model

## Setup

This is a Phase 0 paper-modeling exercise. Do not write SQL. Work in markdown.

## Given

A migration team imports legacy customers and orders in batches. Legacy identifiers are not globally unique, and several source rows may refer to the same real customer. Reviewers need to trace which import batch produced each mapping decision.

## Task

Identify candidate entities and relationships from the scenario. Produce a short markdown list with entity names and relationship names. Note that this uses the modeling variant of the paper-modeling rubric.

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

- Lists candidate entities from the prose scenario.
- Names at least two relationships in ordinary language.
- Avoids SQL syntax and database-object terminology.
## Estimated Time

10 minutes.
