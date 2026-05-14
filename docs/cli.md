# pgfound CLI

The `pgfound` CLI is the stable orchestration surface for PostgreSQL Foundations.
Some commands are intentionally stubs and name the future prompt that completes
them.

## `pgfound --help`

Shows the root command group and available command groups.

## `pgfound version`

Prints the installed `pgfound` package version.

## `pgfound doctor`

Checks the local Python version, Docker CLI availability, required repository
directories, and whether `docker compose config` parses under `docker/`. Results
are rendered as a Rich table and the command exits non-zero when a required
check fails.

## `pgfound lab up`

Starts the primary Docker Compose lab.

Options:

- `--foreground`: run Compose in the foreground instead of detached mode.

## `pgfound lab sandbox-up`

Starts the sandbox Compose profile.

Options:

- `--foreground`: run Compose in the foreground instead of detached mode.

## `pgfound lab down`

Stops the Docker Compose lab.

Options:

- `--volumes`: remove named Docker volumes too.

## `pgfound lab nuke`

Stops the Docker Compose lab and removes lab volumes.

## `pgfound lab psql`

Execs into an interactive `psql` session inside the lab container.

Options:

- `--user`: PostgreSQL role to connect as. Defaults to `pgfound`.
- `--db`: PostgreSQL database to connect to. Defaults to `pgfound`.

## `pgfound lab logs [SERVICE]`

Shows Docker Compose logs for all services or one optional service.

Options:

- `--follow`, `-f`: follow log output.

## `pgfound lab status`

Runs `docker compose ps --format json` and renders service status as a Rich table.

## `pgfound lab concurrency list`

Lists concurrency scenario YAML files under `scenarios/concurrency/`.

## `pgfound lab concurrency run SCENARIO_YAML`

Runs one deterministic multi-session scenario against the lab database. The
command executes setup SQL, opens the declared sessions, walks the ordered
steps, verifies row, rowcount, error-code, and blocking expectations, and exits
non-zero on mismatch.

Options:

- `--on-fail [close|pause]`: with `pause`, hold the harness connections open
  after a mismatch until Enter is pressed, so the operator can inspect from
  another `psql`.

## `pgfound lab concurrency record SCENARIO_YAML`

Runs a scenario and prints a normalized JSON transcript for authoring review.

## `pgfound lab reset-domain DOMAIN`

Drops and recreates one teaching domain schema, then reseeds that domain to the
latest available phase.

## `pgfound lab snapshot NAME`

Writes a custom-format `pg_dump` of the `pgfound` database to
`tmp/snapshots/<name>.dump`.

## `pgfound lab restore NAME`

Restores `tmp/snapshots/<name>.dump` into the `pgfound` database with
`pg_restore --clean --if-exists --no-owner`.

## `pgfound ops query NAME`

Runs one canonical monitoring SQL script from `scripts/monitoring/` against the
configured lab database and renders the rowset as a Rich table. Available names
include `top-by-total-time`, `blocking-chain`, `unused-indexes`, `replica-lag`,
and `table-sizes`.

## `pgfound content list`

Lists content IDs, placeholder titles, and file paths.

Options:

- `--kind [lesson|exercise|scenario|capstone|rubric]`: restrict listing to one
  content kind. If omitted, all content kinds are listed.

## `pgfound content show KIND ID`

Prints raw file content for one content item. Structured loading lands in
`PROMPT_05`.

## `pgfound content validate`

Validates authored JSON/YAML content against the schemas in `content-schemas/`
and runs cross-file checks for lesson, exercise, rubric, scenario, and capstone
references. The command prints a Rich table grouped by content kind, lists any
errors or warnings, and exits non-zero on errors.

By default it walks the real content directories: `lessons/`, `exercises/`,
`rubrics/`, `scenarios/`, `capstones/`, plus `curriculum/map.json`. It skips
`content-schemas/examples/`.

Options:

- `--include-examples`: also validate the five schema example files.
- `--paths GLOB`: restrict validation to one glob or file path. May be provided
  more than once.
- `--strict`: treat warnings as errors.

## `pgfound content scaffold lesson`

Creates a draft lesson directory under `lessons/` from the lesson templates.
The command resolves the phase directory from `curriculum/map.json`, writes
`lesson.json` and `body.md`, then validates the scaffolded draft.

Required options:

- `--phase`: numeric phase.
- `--cluster`: cluster slug.
- `--slug`: lesson slug and ID.
- `--title`: lesson title.
- `--capability-layer`: capability layer slug.

## `pgfound content scaffold exercise`

Creates a draft exercise directory under root `exercises/` and validates the
generated metadata with its parent lesson.

Example:

```sh
uv run pgfound content scaffold exercise \
  --lesson phase-07/index-fundamentals/btree-composite-vs-single-column \
  --level c \
  --slug analyze-composite-plan \
  --kind query \
  --title "Analyze a composite B-tree plan"
```

Required options:

- `--lesson`: path to the lesson directory under `lessons/`.
- `--level`: scaffolding level `a`, `b`, `c`, or `d`.
- `--slug`: exercise slug and ID.
- `--kind`: one of `query`, `schema`, `modeling`, `debug`, `critique`, or `lab`.
- `--title`: exercise title.
- `--sessions`: number of psql sessions for a multi-session exercise. Defaults
  to `1`; values above `1` emit a trace template and session script files.

## `pgfound content lint`

Runs lesson authoring lint checks: required body sections, active body length,
bare URLs, and TODO/TBD/XXX tokens in active content. It also scans exercise
`solution.sql` files for known SQL constructs that appear in
`not_yet_allowed_concepts`, such as `OVER (...)` for `window_function`.

Options:

- `--paths GLOB`: restrict lint to one glob or file path. May be provided more
  than once.
- `--strict`: exit non-zero when warnings are present.

## `pgfound content seed DOMAIN`

Loads a reusable domain seed pack from `seed-data/packs/` into the PostgreSQL
lab. The command connects with `PGFOUND_DB_URL` when set; otherwise it uses the
compose defaults from `pgfound.config`. SQL files are executed in curriculum
phase order and are written to be idempotent.

Example:

```sh
uv run pgfound content seed ecommerce --phase 1 --dry-run
uv run pgfound content seed ecommerce --phase 1 --reset
```

Options:

- `--phase PHASE`: run SQL up to a phase ID such as `1`, `2`, `4a`, or `7b`.
  If omitted, all available phase SQL for the domain runs.
- `--reset`: drop and recreate the domain schema before loading the selected
  SQL files.
- `--generate`: run any deterministic pack generators before seeding. Packs
  without generators treat this as a no-op.
- `--dry-run`: print the SQL files that would run and exit without connecting
  to PostgreSQL.

## `pgfound content seed-doctor`

Scans every exercise, confirms its referenced seed phase SQL exists, and checks
that tables referenced from executable `solution.sql` files appear in the seed
pack SQL. Issues are rendered as a Rich table and the command exits non-zero on
drift.

## `pgfound exercise run EXERCISE_ID`

Prints an exercise prompt, shows the seed pack plan and search path, and opens an
interactive `psql` session inside the lab container. Exercise IDs can be passed
as bare slugs when unique, or as a path under `exercises/` when disambiguation is
needed.

Example:

```sh
uv run pgfound exercise run first-select-write-query --dry-run
uv run pgfound exercise run first-select-write-query --auto-seed
uv run pgfound exercise run first-select-write-query --check
```

Options:

- `--auto-seed`: reset and load the exercise seed pack before opening `psql`.
- `--dry-run`: print the prompt and seed plan without touching Docker.
- `--check`: compare `tmp/answers/<exercise-id>.sql` with the reference
  `solution.sql` by canonicalized row output. For `multi_session_trace`
  exercises, this runs the scenario named by `lab_harness_profile` and splices
  the learner SQL into `${LEARNER_SQL}` when the scenario declares that
  placeholder.
- `--answer PATH`: check this SQL file instead of the default answer path.
- `--no-prompt`: skip printing the prompt.
- `--save-answer`: best-effort copy of the last statement from `~/.psql_history`
  into the canonical answer path after the psql session.

## `pgfound exercise review EXERCISE_ID --answer PATH`

Runs the mechanical review engine for one exercise answer, writes Markdown and
JSON reports under `tmp/reviews/<exercise-id>/`, and prints the scored rubric
summary plus findings.

```bash
uv run pgfound exercise review first-select-write-query --answer tmp/answers/first-select-write-query.sql --auto
uv run pgfound exercise review what-lateral-unlocks-level-c-1 --answer exercises/phase-05-expressive-querying/what-lateral-unlocks/level-c/what-lateral-unlocks-level-c-1/solution.sql --full
```

`--auto` runs correctness comparison. `--full` also attempts plan comparison
against the live lab database.

## `pgfound progress show`

Reads `tmp/progress/` and prints a Rich progress dashboard with phase, admin,
extension, capstone, interview, and recent-attempt signals.

```bash
uv run pgfound progress init --name "test"
uv run pgfound progress show
uv run pgfound progress show --module phase-01
uv run pgfound progress export --format markdown
```

## `pgfound remediate`

Builds a remediation pack under `tmp/remediation/` from weak rubric dimensions,
skipped Level D work, and unmet module exit evidence.

```bash
uv run pgfound remediate
uv run pgfound remediate --module phase-06 --scope all
```

## `pgfound next`

Recommends one next learner action with a one-sentence rationale.

```bash
uv run pgfound next
```

## `pgfound coach report PROFILE_PATH`

Prints a coach-friendly Markdown progress report for a local profile.

```bash
uv run pgfound coach report tmp/progress/profile.json
```

## `pgfound capstone start ID`

Copies `capstones/<ID>/starter/` into `tmp/capstone-work/<ID>/`, prints the
capstone brief, constraints, and acceptance criteria, and registers a started
attempt under `tmp/progress/capstones/<ID>.json`.

## `pgfound capstone evaluate ID --path DIR`

Runs the capstone review engine for a learner workspace, scores mechanically
observable rubric dimensions, and writes reports under
`tmp/reviews/capstone/<id>/`.

`--full` uses the sandbox database URL (`PGFOUND_SANDBOX_DB_URL`, otherwise
compose defaults on port 55434), applies schema/index/RLS artifacts in a
rollback, executes reference and learner critical-query files, and compares
normalized outputs.

## `pgfound review run`

Generic review entry point. Provide exactly one target:

```bash
uv run pgfound review run --exercise-id first-select-write-query --answer tmp/answers/first-select-write-query.sql
uv run pgfound review run --capstone-id 01-multi-tenant-saas-crm --path capstones/01-multi-tenant-saas-crm/reference --full
```

## `pgfound decision run`

Validates a decision-engine intake JSON document, loads the current catalog and
rule directories, and writes `report.json` plus `report.md`.

```bash
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json
uv run pgfound decision run decision-engine/fixtures/intakes/saas-multi-tenant-minimal.json --out-dir tmp/my-report
uv run pgfound decision from-progress
```

The prompt-39 implementation is intentionally conservative: catalogs and rules
are not authored yet, so valid intakes produce an empty valid report with
warnings that the catalog and rule data is not yet available. Validation errors
exit non-zero and print the failing schema paths.

## `pgfound interview start`

Stub command that exits 0 and reports that the interview simulator lands in
`PROMPT_28`.
