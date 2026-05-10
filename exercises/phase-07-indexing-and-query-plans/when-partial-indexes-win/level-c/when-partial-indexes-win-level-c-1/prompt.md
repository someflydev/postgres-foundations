# When Partial Indexes Win Level C1

Demonstrate that a broad status index is not the right fix for the hot pending-orders dashboard, then create a partial index WHERE status = 'pending' and compare the plan with pgfound lab explain.

Record the before and after plan and explain the maintenance tradeoff.
