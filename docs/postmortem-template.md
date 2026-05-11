# Database Incident Postmortem Template

## Summary

State what happened, when it started, when it ended, and which user-visible capability was affected.

## Invariant Violated

Name the database invariant that failed: latency, durability, freshness, availability, access boundary, or capacity.

## Blast Radius

List affected tenants, tables, services, jobs, and operational workflows.

## Detection Latency

Record when the first signal appeared, when humans noticed, and why detection was fast or slow.

## Mitigation

Describe the immediate action, the PostgreSQL evidence used, and the verification query or metric.

## Durable Fix

Name the schema, query, configuration, process, or alerting change that prevents recurrence.

## Follow-Up Owners

Assign each action to an owner and a due date.
