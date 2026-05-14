# Decision Engine Known Edges

The decision engine is explainable planning support, not an autonomous
architecture authority. It turns structured workload signals into a reviewable
PostgreSQL recommendation. Humans still own context, implementation sequence,
budget, risk tolerance, and final acceptance.

## Current Boundaries

- Inputs are only as good as the intake. Missing scale, tenancy, security,
  migration, and operations signals will produce conservative guidance.
- Rules are catalog-backed but not exhaustive. They cover the repo's current
  core features, extensions, index patterns, topology patterns, and
  anti-patterns.
- Scores support triage. They are not a substitute for benchmark results,
  production telemetry, restore drills, or security review.
- "Candidate later" is intentionally not approval. It means there is a plausible
  future path if the named trigger signals appear.
- "Avoid for now" warnings are posture checks. They should be resolved before a
  team adds complexity, not treated as a permanent rejection.

## Review Expectations

When a report feels surprising, inspect the cited rules, catalog entries,
follow-up questions, and score breakdown before changing behavior. Prefer
tightening an intake or rule trigger over broad score manipulation. Any new
recommendation path should name the workload signal, the operational burden,
the portability consequence, and the evidence that would reverse the decision.

For scenario coverage, run:

```bash
uv run pgfound decision scenarios audit
```

For rule validation, run:

```bash
uv run pgfound decision rules lint
```
