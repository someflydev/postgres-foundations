# Repo Layout

- `.context/` contains short agent-facing notes about current scaffold state,
  prompt progress, runbooks, and indexes into canonical docs.
- `.prompts/` contains the authoritative monotonic build sequence for the
  repository.
- `capstones/` will contain integrated assessments that require learners to
  combine SQL, design, debugging, operations, and defense.
- `curriculum/` will contain phase and module structure for the training
  system.
- `decision-engine/` will contain planning catalogs, rules, prompt packs,
  scoring inputs, and report-generation artifacts.
- `docker/` will contain the canonical reproducible PostgreSQL lab
  environment.
- `docs/` contains doctrine, architecture, repo maps, LLM guidance, and ADRs.
- `exercises/` will contain learner tasks and lab prompts.
- `lessons/` will contain instructional material for the curriculum phases and
  advanced tracks.
- `llm-prompts/` will contain training-side prompts for coaching, review,
  interviews, adversarial critique, and remediation.
- `rubrics/` will contain review criteria and assessment standards.
- `scenarios/` will contain realistic failure, design, workload, and operations
  situations.
- `scripts/` will contain repository automation and verification helpers.
- `seed-data/` will contain lab datasets and fixtures.
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
planning workflows. Doctrine belongs in `docs/doctrine.md`; later lessons,
rules, and rubrics should point back to it instead of restating it.
