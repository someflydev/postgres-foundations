# Repair the Repairing a Paper Model model

## Setup

This is a Phase 0 paper-modeling exercise. Do not write SQL. Work in markdown.

## Given

A knowledge base stores documents written by authors and organized by tags. Documents move through draft, published, revised, and archived states. A document may have several tags, and the same tag can belong to many documents.

The flawed model says: tag labels are stored as one comma-separated document attribute; author names are copied into every document revision; publication state can be any phrase; documents have no revision events; archived documents lose their original publication date.

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
