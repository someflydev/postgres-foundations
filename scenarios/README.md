# Industry Scenarios

The `scenarios/industries/` tree contains field-style scenario packs used by the curriculum, capstones, interview simulator, and decision-engine regression tests. Each pack includes a human narrative, a structured scenario manifest, a decision intake, and golden JSON/Markdown reports generated from the current decision engine.

Use `uv run pgfound decision golden-refresh --confirm` after intentional catalog or rule changes. `uv run pgfound content validate` checks that each golden still matches the engine output, ignoring dynamic report metadata such as generation time.

## Industry Coverage

Batch 1 scenarios cover SaaS multi-tenant, fintech payments, healthcare ops, and ecommerce marketplace.

Batch 2 scenarios cover:

- `logistics-geo`: single-city last-mile delivery, multi-region service zones, and global fleet analytics.
- `observability-iot`: internal observability, IoT fleet telemetry, and incident operations.
- `knowledge-ai`: engineering knowledge search, support assistant retrieval, and research-corpus hybrid retrieval.
- `modernization-bridge`: monolith carveout, multi-database consolidation, and near-zero-downtime major upgrade.

Use `uv run pgfound decision scenarios audit` to see extension recommendation coverage across all industry scenario packs.
