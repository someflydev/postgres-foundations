# Scenario Review Checklist

Use this checklist for industry scenarios, concurrency scenarios, capstone
scenarios, and interview scenarios.

## Scenario Contract

- The scenario has a clear user, system context, workload shape, and constraint
  set.
- Data, scale, tenancy, security, migration, and operations signals are
  specific enough to drive review.
- The scenario avoids hidden assumptions that only the author can infer.
- Narrative detail supports decisions rather than filling space.

## Artifact Integrity

- `scenario.json` resolves suggested lessons, exercises, capstones, and
  rubrics.
- Industry scenarios include a valid intake and current expected reports.
- Concurrency scenarios can be replayed deterministically enough to teach the
  intended anomaly or lock behavior.
- Interview scenarios map stages to realistic follow-up prompts.

## Doctrine Alignment

- The scenario makes PostgreSQL core alternatives visible.
- Extension, topology, or sharding pressure is tied to signals.
- "Not yet" outcomes are acceptable and should be represented when realistic.

## Review Output

Approve when the scenario can be run or reviewed by someone other than the
author. If it cannot, ask for missing signals, tighter artifacts, or a smaller
scenario.
