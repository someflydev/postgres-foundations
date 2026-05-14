# Progress and Remediation

The learner loop is:

1. `pgfound progress init --name <name>`
2. `pgfound next`
3. Do the recommended lesson, exercise, interview, or capstone work.
4. Run the relevant check or review command.
5. `pgfound progress show`
6. `pgfound remediate` when the evidence shows repeated weak dimensions.
7. Repeat.

Progress lives in `tmp/progress/` and is intentionally local. The platform is
not a hosted LMS; it is a self-study record that can be exported for a coaching
conversation with `pgfound progress export`.

Module progress is evidence-based. A phase, admin module, or extension module is
`met` when its lesson clusters have passing Level D evidence. Anything touched
but not complete is `in-progress`; untouched modules are `not-started`.

`pgfound remediate` builds a compact remediation pack under `tmp/remediation/`.
The pack lists lessons to re-read, Level D exercises to complete, and a rendered
failure-lab prompt from the remediation prompt templates. The prompt is saved so
a learner or coach can run it against their preferred LLM without the CLI making
provider calls.

`pgfound next` is the daily command. It chooses one action and gives a short
rationale based on unmet module evidence, weak rubric dimensions, interview
practice, or capstone synthesis.

`pgfound decision from-progress` is a showcase workflow for a learner who wants
to practice as an architect. It creates a decision-engine intake from the local
profile and progress shape, then the normal decision-engine commands can review
that intake.
