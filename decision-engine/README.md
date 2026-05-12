# Decision Engine

The decision engine turns structured workload intakes into explainable
PostgreSQL planning reports. It is core-first: extensions and complex topology
choices require workload evidence, operational readiness, portability review,
and explicit triggers for later adoption.

- `architecture.md` describes the subsystem boundaries and processing model.
- `schemas/` contains draft-2020-12 JSON Schemas for intakes, catalogs, rules,
  recommendations, and reports.
- `catalogs/` will hold authored catalog data in PROMPT_40 and PROMPT_41.
- `rules/` will hold matching and scoring rules in PROMPT_42.
- `prompts/` will hold planning prompt packs in PROMPT_44.
- `fixtures/intakes/` contains small but realistic intake examples.
- `fixtures/reports/` is reserved for golden reports in PROMPT_43.

Run the current stub with:

```bash
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json
```
