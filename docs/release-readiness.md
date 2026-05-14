# Release Readiness

Use this checklist before declaring a milestone release.

- [ ] All `.prompts/PROMPT_*.txt` files are accounted for in `.context/prompt-log.md`.
- [ ] All ADRs have a status.
- [ ] Any `Proposed` ADR has an owner and expected-by date.
- [ ] `scripts/verify-all.sh` exits 0.
- [ ] Integration tests pass locally against the `pg` profile.
- [ ] Extension-profile tests pass when PostGIS, pgvector, TimescaleDB, and Citus profiles are available.
- [ ] The decision engine's golden reports match `uv run pgfound decision golden-refresh --dry-run`.
- [ ] The `README.md` quickstart block has been run from scratch by a human in the last 30 days.
- [ ] Known gaps are captured in `docs/known-gaps.md` with owner notes.

When a maintainer decides to cut the release:

```bash
git tag -a v0.1.0 -m "Initial release of postgres-foundations"
```
