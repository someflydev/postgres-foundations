# Solution

A materialized view is a cached result, not a source of truth. If
`events.hourly_event_counts` was refreshed at 01:00 and the incident review is
run at 01:45, the materialized view cannot show event rows inserted after the
refresh. Treating it as authoritative hides recent spikes and produces stale
operational decisions.

The diagnosis should include three facts:

- The base table `events.events` is the source of truth.
- The materialized view is useful only for reports that tolerate its refresh
  lag.
- The refresh policy is part of the design, not an implementation footnote.

A defensible repair is either:

```sql
REFRESH MATERIALIZED VIEW events.hourly_event_counts;
```

on a schedule aligned with the report's freshness requirement, or a switch to a
regular view / inline aggregate when the report must always reflect committed
base-table rows. If readers need the materialized view during refreshes, the
team can plan for `REFRESH MATERIALIZED VIEW CONCURRENTLY` later, but that also
requires the materialized view to have an appropriate unique index. The Phase 5
answer should focus on the staleness tradeoff and the ownership of refresh
timing.
