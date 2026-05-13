# Decision Engine

The decision engine turns structured workload intakes into explainable
PostgreSQL planning reports. It is core-first: extensions and complex topology
choices require workload evidence, operational readiness, portability review,
and explicit triggers for later adoption.

- `architecture.md` describes the subsystem boundaries and processing model.
- `schemas/` contains draft-2020-12 JSON Schemas for intakes, catalogs, rules,
  recommendations, and reports.
- `catalogs/` holds authored catalog data for industries, data shapes,
  workload patterns, core features, extensions, index patterns, topology
  patterns, and anti-patterns.
- `rules/` holds declarative matching rules and an authoring guide.
- `prompts/` will hold planning prompt packs in PROMPT_44.
- `fixtures/intakes/` contains small but realistic intake examples.
- `fixtures/reports/` contains Prompt 42 report snapshots; PROMPT_43 upgrades
  them into masked golden tests for the scoring and report-generator work.

Run the engine with:

```bash
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json
```

Lint the rule pack with:

```bash
uv run pgfound decision rules lint
```
