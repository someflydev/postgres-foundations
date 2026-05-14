# Rule Review Checklist

Use this checklist for decision-engine rules and rule changes.

## Trigger Quality

- The rule names a concrete workload, data-shape, scale, security, tenancy, or
  migration signal.
- Positive recommendations require enough evidence for "why now".
- Deferred recommendations include "not yet" trigger language.
- Anti-pattern warnings describe what risk the team is creating.

## Catalog Alignment

- Recommendation targets exist in the relevant catalog.
- Rule IDs, slugs, and citations are stable and readable.
- Operational burden and portability effects align with catalog entries.
- The rule does not duplicate another rule unless the trigger is materially
  different.

## Report Behavior

- Fixture changes are intentional and reviewed in Markdown, not only JSON.
- Score changes improve explanation quality rather than forcing a desired
  verdict.
- Follow-up questions help resolve missing evidence.

## Review Output

Ask for a scenario or fixture when a rule introduces a new recommendation path.
Reject rules that recommend complexity because it is interesting rather than
because the workload signals justify it.
