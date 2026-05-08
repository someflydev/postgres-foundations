# Repair the Naming Things That Exist model

## Setup

This is a Phase 0 paper-modeling exercise. Do not write SQL. Work in markdown.

## Given

A SaaS product serves many customer organizations. Users belong to tenants and may have roles on several projects inside the same tenant. The team needs to avoid mixing facts from different tenants while still recognizing the same person by email inside a tenant.

The flawed model says: project names are globally unique across all tenants; user role is stored once on the user; tenant name is copied onto every project note; memberships are not modeled; user removal deletes the history of prior project access.

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
