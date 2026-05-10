# GIN Cost Model Level D1

You inherit a broad JSONB GIN index on an event table with heavy writes and
rare containment searches. Diagnose whether the index has a poor
bloat-to-value ratio. Compare query benefit against build cost, write cost,
pending-list behavior, and simpler alternatives such as a scalar column or a
narrow expression index.

Record the before and after plan and explain the maintenance tradeoff.
