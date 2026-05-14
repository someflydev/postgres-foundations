# Contributing

## How This Repo Thinks About Contributions

Contributions need to align with the repo doctrine. Do not add a feature,
extension, topology, or teaching path only because it is interesting. Every PR
should cite a line from [docs/doctrine.md](docs/doctrine.md) or name a concrete
learner, reviewer, architect, or team need.

Prefer small, reviewable changes. Keep content, code, fixtures, and docs in
sync. If a change alters behavior, include tests or explain why the existing
checks already cover it.

## Authoring Content

Lesson authors should start with [docs/authoring-lessons.md](docs/authoring-lessons.md).
Exercise authors should start with [docs/authoring-exercises.md](docs/authoring-exercises.md).
Use [docs/authoring.md](docs/authoring.md) for shared content expectations.

## Authoring Decision-Engine Content

Decision-engine changes should follow the four-layer prompt pack under
`decision-engine/prompts/`. Catalog changes belong with
`decision-engine/catalogs/README.md`; rule changes belong with
`decision-engine/rules/README.md`; scenario changes should also use
[docs/decision-engine-scenarios.md](docs/decision-engine-scenarios.md).

## Dev Setup

```bash
uv sync
uv run pgfound doctor
uv run pre-commit install
make fmt
make lint
make test
```

The pre-commit setup runs Ruff, light YAML checks for workflow and compose
files, staged-file content validation, docs checks for staged Markdown files,
and standard whitespace/file-size guards. To run the same hooks manually:

```bash
uv run pre-commit run --all-files
```

## Commit And PR Hygiene

Use imperative subject lines. Prefer scope prefixes such as
`feat(decision-engine):`, `fix(review):`, `docs(admin):`, or `test(content):`.

Before opening a PR, run:

```bash
make verify
```

PRs should include the user need, changed artifacts, verification commands, and
any intentionally changed golden files or scenario reports. CI must pass before
merge once CI exists.

## Adding A New Extension Module

- Update `curriculum/extensions/map.json`.
- Add or update the extension catalog entry in `decision-engine/catalogs/extensions.json`.
- Add at least one decision rule that can recommend, defer, or warn about the extension.
- Add at least one scenario or fixture that covers the extension path.
- Add lessons under `lessons/extensions/`.
- Add exercises under `exercises/extensions/`.
- Update admin-track cross-references if the extension has operational impact.
- Add a playbook under `docs/extension-track/`.
- Run content validation, content lint, rule lint, and relevant tests.

## Adding A New Industry Or Scenario

- Add the scenario metadata under `scenarios/`.
- Include a narrative when the scenario is used for architecture planning.
- Add or reuse a valid decision-engine intake when planning behavior is involved.
- Generate expected JSON and Markdown reports when the scenario is a regression fixture.
- Link suggested lessons, exercises, and capstones only when those artifacts exist.
- Update [docs/decision-engine-scenarios.md](docs/decision-engine-scenarios.md) if the scenario changes coverage expectations.
- Run `uv run pgfound decision scenarios audit` and `uv run pgfound content validate`.

## Code Of Conduct

Be direct, specific, and respectful. Critique artifacts and arguments, not
people. No harassment, personal attacks, or bad-faith participation. If a
dedicated `CODE_OF_CONDUCT.md` is added later, it becomes the authoritative
policy.

## Reporting Issues

Include the command you ran, the expected behavior, the actual behavior, your
environment, and the smallest input or fixture that reproduces the issue. For
content issues, include the lesson, exercise, rule, scenario, or doc path.
