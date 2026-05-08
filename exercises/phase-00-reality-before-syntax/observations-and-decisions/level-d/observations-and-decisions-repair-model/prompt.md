# Repair the Observations and Decisions model

## Setup

This is a Phase 0 paper-modeling exercise. Do not write SQL. Work in markdown.

## Given

A clinic schedules appointments between providers and clients. Providers have specialties and bookable availability windows. Appointments move from requested to confirmed, canceled, or completed, and the office needs to know who changed the appointment state.

The flawed model says: provider name is plain text on each appointment; clients are identified only by phone number; appointment status can skip from requested to completed; availability windows are not related to providers; cancellations overwrite the original appointment request.

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
