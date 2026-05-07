# JSON First Content Model

## Status

Accepted

## Date

2026-05-07

## Context

The platform will contain curriculum metadata, rubric structures,
decision-engine catalogs, rules, scoring inputs, anti-pattern definitions, and
reporting data. These artifacts must be reviewable by humans and validated by
programs. They will also drive automated review, prompt assembly, and planning
reports, so the format must support stable diffs and predictable parsing.

## Decision

Use JSON as the default structured data format for content metadata and
decision-engine data. YAML is tolerated only where human ergonomics clearly
demand it, and those cases should remain narrow. Canonical catalogs and rules
should prefer JSON schemas or equivalent validation as the platform matures.

## Consequences

JSON-first data is easy to parse consistently from Python and other tooling,
works well with validation, and produces explicit structural diffs. Authors
lose YAML conveniences such as comments and relaxed syntax in most structured
artifacts, but the tradeoff is justified by the need for automated checks and
machine-readable planning output. Documentation can explain intent around JSON
data instead of embedding comments inside the data files.

## Alternatives considered

YAML-first content was rejected because implicit typing, parser differences,
and formatting variance add risk to validation-heavy workflows. Markdown-only
metadata was rejected because it is difficult to validate and reuse in scoring
or report generation. Database-backed authoring was deferred because the early
repository needs transparent files and reviewable changes.

## Related ADRs/docs

- [Architecture](../architecture.md)
- [Repo layout](../repo-layout.md)
