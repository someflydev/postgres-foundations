# LLM Prompt Templates

This directory contains provider-agnostic prompt templates rendered by the
`pgfound llm` CLI. Training-side templates live under `coaching/`, `critique/`,
and `remediation/`. Interview stage stubs under `interview/stages/` predate
this format and are upgraded separately.

Render a template without sending it to any model:

```bash
uv run pgfound llm render critique/query-critique \
  --context tests/fixtures/critique-context.json
```

The rendering contract is intentionally plain Markdown plus YAML front matter.
The platform records rendered prompts as audit artifacts before any future LLM
dispatch layer is allowed to send them.
