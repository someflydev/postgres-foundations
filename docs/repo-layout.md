# Repo Layout

- `.context/` contains short agent-facing notes, prompt progress, runbooks, and
  indexes into canonical docs.
- `.prompts/` contains the historical monotonic build sequence for the
  repository.
- `capstones/` contains integrated assessments that require learners to combine
  SQL, design, debugging, operations, and defense.
- `curriculum/` contains phase and module structure for the training system.
- `decision-engine/` contains planning catalogs, rules, schemas, prompt packs,
  scoring inputs, fixtures, golden reports, and report-generation artifacts.
- `docker/` contains the canonical reproducible PostgreSQL lab environment.
- `docs/` contains doctrine, architecture, repo maps, LLM guidance, and ADRs.
- `exercises/` contains learner tasks and lab prompts for phases, admin modules,
  and extensions.
- `lessons/` contains instructional material for curriculum phases and advanced
  tracks.
- `llm-prompts/` contains training-side prompts for coaching, review,
  interviews, adversarial critique, and remediation.
- `rubrics/` contains review criteria and assessment standards.
- `scenarios/` contains realistic failure, design, workload, interview,
  capstone, concurrency, and industry-planning situations.
- `scripts/` contains repository automation and verification helpers.
- `seed-data/` contains lab datasets and fixtures.
- `src/` contains the Python package and command-line implementation.
- `tests/` contains automated tests for package behavior, validation, and later
  platform checks.
- `tmp/` is a scratch location for local work that should not become canonical
  project content.

## Things That Live in Multiple Places on Purpose

Some concepts appear in more than one subsystem, but only one place should own
the metadata. For example, the extension catalog should be authoritative in
`decision-engine/catalogs/extensions.json` and referenced from extension track
lessons or rubrics. Prompt templates are intentionally split between
`llm-prompts/` for training workflows and `decision-engine/prompts/` for
planning workflows. Doctrine belongs in `docs/doctrine.md`; lessons, rules, and
rubrics should point back to it instead of restating it.
