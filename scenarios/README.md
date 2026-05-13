# Industry Scenarios

The `scenarios/industries/` tree contains field-style scenario packs used by the curriculum, capstones, interview simulator, and decision-engine regression tests. Each pack includes a human narrative, a structured scenario manifest, a decision intake, and golden JSON/Markdown reports generated from the current decision engine.

Use `uv run pgfound decision golden-refresh --confirm` after intentional catalog or rule changes. `uv run pgfound content validate` checks that each golden still matches the engine output, ignoring dynamic report metadata such as generation time.
