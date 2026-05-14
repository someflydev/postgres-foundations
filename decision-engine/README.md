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
- `prompts/` contains the four-layer planning prompt pack for catalog,
  evaluator, scenario, and critique work.
- `fixtures/intakes/` contains small but realistic intake examples.
- `fixtures/reports/` contains golden JSON and Markdown reports for every
  fixture intake.

Run the engine with:

```bash
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json
```

The default `--format both` writes `report.json` and `report.md` under
`tmp/decision-reports/<intake-id>/<timestamp>/`. Use `--format json` to emit
only JSON to stdout, or `--format markdown --show-scores` to emit the
architect-facing report with the score table.

Read the Markdown report in this order:

1. Start with `Summary` to understand the posture: what is ready now, what is
   deferred, and whether anti-patterns matched.
2. Review `Recommend now` as the proposed 90-day implementation surface.
3. Treat `Candidate later` as a backlog of evidence-gathering work, not as a
   hidden approval.
4. Use `Not enough evidence` and grouped follow-up questions to improve the
   intake before making a high-cost decision.
5. Resolve `Avoid for now` warnings before adding extensions, topology, or
   index complexity.
6. Check `Score breakdown` when a recommendation feels surprising. Penalty
   columns are positive values that reduce the aggregate score.

Lint the rule pack with:

```bash
uv run pgfound decision rules lint
```

Compare two reports with:

```bash
uv run pgfound decision diff report-a.md report-b.md
```

Regenerate golden reports only when the report change is intentional:

```bash
scripts/update-decision-goldens.sh --confirm
uv run pytest tests/test_decision_golden.py tests/test_report_writer.py -q
```
