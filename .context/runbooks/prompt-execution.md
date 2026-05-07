# Prompt Execution

Fresh sessions usually start with: "Load AGENT.md, then run
`.prompts/PROMPT_XX.txt`." Treat that as instruction to load this context, read
the named prompt, and execute only that prompt.

## Run A Prompt

1. Read the requested prompt from `.prompts/` completely.
2. Run the prompt's prior-work checks before editing.
3. Stop and inspect carefully if the repo already contains artifacts that the
   prompt assumes do not exist.
4. Make only the changes requested by the current prompt.
5. Run the prompt's verification commands.
6. Report the result, including commands that could not be run.

Do not infer permission to run the next prompt from a successful verification.

## Review A Completed Prompt

After a prompt run, the user often asks: "Does everything look appropriately
implemented for PROMPT_XX? Do not run PROMPT_XX+1, but look at it to make sure
it is set up for success."

When that happens:

1. Re-check the completed prompt's requirements against the repo state.
2. Read the next prompt only to understand its prerequisites.
3. Do not implement the next prompt.
4. Run lightweight verification for the completed prompt when useful.
5. Report any gaps, risks, or setup issues plainly.

If a fix is needed, the user may ask for a quick plan and inline fix. Keep the
plan short, make the focused correction, and rerun the relevant checks.

## Context Maintenance

Before grouped commit suggestions, check whether `AGENT.md` or `.context/`
should be updated to reflect durable repo conventions, canonical docs, commands,
ADRs, schemas, or workflow changes introduced by the prompt.

Do not update context just because a prompt ran. Prefer links and short indexes
to duplicating canonical content from `docs/`, `decision-engine/`, or other
source directories.

## Commit Suggestions

The user may ask for grouped Tim Pope style multi-line commits. When asked:

1. Inspect `git status` and relevant diffs.
2. Group related hunks into easy-to-review commits. Use `git add -p` when a
   file contains changes that belong in different commits.
3. Prefix each commit subject with `[PROMPT_XX]`.
4. Use concise imperative subjects and explanatory bodies.
5. Use heredoc `EOF` commit messages so literal `\n` sequences do not appear in
   the commit string.
6. Do not include a co-author section.

Example shape:

```sh
git commit -F - <<'EOF'
[PROMPT_XX] Add scaffolded project tooling

Create the uv project metadata, package entry point, and helper commands needed
for the prompt baseline.
EOF
```

Do not create commits unless the user asks to actually commit. If they ask only
for suggestions, provide grouped commands and explain any `git add -p` grouping
that should happen before each commit.
