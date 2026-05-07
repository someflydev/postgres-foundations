# Architecture Decision Records

This directory contains Architecture Decision Records for
`postgres-foundations`. An ADR records a durable project decision, the context
that made it necessary, the consequences of the choice, and the alternatives
that were considered.

ADR filenames use a monotonic numeric prefix and a short lowercase title:

```text
NNNN-short-title.md
```

Numbers are never reused. New ADRs should use the next available number even if
an earlier ADR is superseded.

## Status Lifecycle

`Proposed` means the decision is being discussed but should not yet be treated
as binding.

`Accepted` means the repository should follow the decision.

`Superseded` means a later ADR replaced the decision. A superseded ADR should
link to the ADR that replaced it.

Each ADR should use `template.md` and fill every section: Title, Status, Date,
Context, Decision, Consequences, Alternatives considered, and Related
ADRs/docs.
