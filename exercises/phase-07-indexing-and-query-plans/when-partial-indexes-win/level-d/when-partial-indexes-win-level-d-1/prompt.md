# When Partial Indexes Win Level D1

A team created a partial index with `WHERE status = 'pending'`, but the
dashboard query is written as `status <> 'delivered'`. Use `pgfound lab
explain` to show why the partial index is never used, then rewrite the query or
recommend a different partial predicate that matches the real workflow.

Record the before and after plan and explain the maintenance tradeoff.
