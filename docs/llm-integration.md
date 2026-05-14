# LLM Integration

`pgfound` renders prompts but does not send them to an LLM provider. This keeps
the training platform provider-agnostic and makes every model payload auditable.

Render a prompt to a file:

```bash
uv run pgfound llm render critique/query-critique \
  --context tests/fixtures/critique-context.json \
  --out tmp/preview.md
```

Pipe a rendered prompt into any LLM CLI you trust:

```bash
uv run pgfound llm render critique/query-critique \
  --context tests/fixtures/critique-context.json \
  | your-llm-cli
```

Override default variables at render time:

```bash
uv run pgfound llm render critique/query-critique \
  --context tests/fixtures/critique-context.json \
  --var max_feedback_items=3
```

The rendered Markdown should be saved with review artifacts before dispatch.
Do not use LLM output as a substitute for running SQL, inspecting plans,
checking constraints, or reproducing concurrency behavior in multiple sessions.
