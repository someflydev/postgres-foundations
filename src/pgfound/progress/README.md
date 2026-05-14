# Progress Data Model

Progress is local learner state under `tmp/progress/`.

- `profile.json` stores `LearnerProfile(name, started_at, goals)`.
- `exercises/<exercise-id>.json` stores canonical exercise attempts with
  timestamps, self-assessment, check result, optional rubric scores, and notes.
- `capstones/<capstone-id>.json` stores started/evaluated capstone attempts.
- `interviews.json` stores reviewed interview attempts.

Writes go through `.tmp` files and `os.replace()` so interrupted writes do not
leave partial JSON at the canonical path.

Derived module progress is not persisted by default. `derive.compute_module_progress()`
loads authored lessons and exercises, then marks a module `met` when each lesson
cluster has at least one passing Level D exercise attempt.
