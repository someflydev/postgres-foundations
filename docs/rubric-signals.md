# Rubric Signals

Rubric signals connect mechanical review runners to human rubrics. A runner
emits a key/value observation, and a rubric dimension maps that observation to a
0-4 score.

```json
{
  "name": "Result semantics",
  "weight": 0.24,
  "signals": [
    {
      "pattern": "output_matches_reference",
      "levels": { "missing": 0, "present": 3 }
    }
  ]
}
```

If no declared signal is present for a dimension, the score is `-1` and the
dimension enters the manual-review queue. The review engine is a coach's
assistant, not a replacement for judgment.

Current signal families include correctness comparison, plan comparison, schema
artifact checks, RLS/index/runbook presence, writeup section lint, extension
posture checks, and concurrency scenario results.

