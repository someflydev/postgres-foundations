# Naive Wall Clock Timestamp

Local wall-clock timestamps are not the same thing as instants in time. Daylight-saving transitions, regional users, integrations, and audit trails make `timestamp without time zone` risky when the application actually needs event time.

This anti-pattern appears when cross-region events, payments, audit entries, or schedules are stored as ambiguous local timestamps. Reports can double-count, miss rows, or sort events incorrectly around timezone changes.

Prefer `timestamptz` for instants and store local schedule intent separately when the business rule is local-time based. For bookings and availability, use range types and explicit timezone rules rather than ad hoc timestamp pairs.
