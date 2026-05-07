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

By default it walks only the real content directories under `curriculum/` and
skips `content-schemas/examples/`.

Options:

- `--include-examples`: also validate the five schema example files.
- `--paths GLOB`: restrict validation to one glob or file path. May be provided
  more than once.
- `--strict`: treat warnings as errors.

## `pgfound review run`

Stub command that exits 0 and reports that the review engine lands in
`PROMPT_27`.

## `pgfound decision run`

Stub command that exits 0 and reports that the decision engine lands in
`PROMPT_43`.

## `pgfound interview start`

Stub command that exits 0 and reports that the interview simulator lands in
`PROMPT_28`.
