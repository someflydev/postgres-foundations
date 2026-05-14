# Exercise Review Checklist

Use this checklist for SQL, schema, critique, multi-session, admin, and
extension exercises.

## Learner Contract

- The prompt asks for one assessable outcome.
- Required files, answer format, seed domain, and lab state are clear.
- The exercise level matches the expected independence: recognition, guided
  production, repair, synthesis, or defense.
- Hints help the learner inspect PostgreSQL behavior without giving away the
  full answer.

## Mechanical Checks

- `exercise.json` resolves its lesson, starter, solution, and rubric paths.
- The solution runs against the intended seed pack and `search_path`.
- Expected output or schema checks are deterministic.
- Multi-session metadata includes enough steps to reproduce the concurrency
  observation.

## Pedagogy And Doctrine

- The exercise practices the lesson capability rather than an unrelated trick.
- Core PostgreSQL features are favored unless the module is explicitly about an
  extension.
- Tradeoff or critique exercises require explanation, not just a final choice.
- Operational exercises ask what can fail and how to verify recovery.

## Review Output

Approve only when the exercise can be run, checked, and explained. Otherwise,
name the smallest fix that would make the learner contract testable.
