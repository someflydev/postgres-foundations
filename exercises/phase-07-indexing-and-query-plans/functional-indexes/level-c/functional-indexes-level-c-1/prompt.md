# Functional Indexes Level C1

Use lower(email) = lower($1) as the workload. Show the plan without a matching expression index, then add an index on lower(email), ANALYZE, and show the plan improvement.

Record the before and after plan and explain the maintenance tradeoff.
