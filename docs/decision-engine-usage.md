# Decision Engine Usage

The decision engine turns a structured PostgreSQL workload intake into a
reviewable architecture recommendation.

## 1. Create or Choose an Intake

Start from a fixture under `decision-engine/fixtures/intakes/` or author a new
JSON document that matches `decision-engine/schemas/intake.schema.json`. The
most important fields are the organization constraints, data shapes, workload
patterns, scale signals, tenancy model, security constraints, migration needs,
existing topology, and free-form notes.

## 2. Run the Engine

Write JSON and Markdown reports to disk:

```bash
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json
```

Emit only JSON for scripts:

```bash
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json --format json
```

Emit the human report with scores:

```bash
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json --format markdown --show-scores
```

## 3. Interpret the Report

Read `report.md` first. `Recommend now` is the proposed near-term adoption
surface. `Candidate later` means the rule matched but the score or operating
model says to wait. `Not enough evidence` means the intake hints at a capability
but does not justify a recommendation. `Avoid for now` contains anti-pattern
warnings, which are surfaced regardless of score.

Use `Score breakdown` to inspect tradeoffs. Domain, data, workload, operations,
and growth increase the aggregate score. Portability and complexity are
penalties, shown as positive table values and subtracted by the scoring model.

## 4. Iterate

Answer the grouped follow-up questions, update the intake, and rerun the engine.
When comparing scenarios, diff the generated Markdown or JSON reports:

```bash
uv run pgfound decision diff tmp/report-a.md tmp/report-b.md
```

When report behavior changes intentionally, regenerate goldens with:

```bash
scripts/update-decision-goldens.sh --confirm
```
