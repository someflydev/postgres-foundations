# GiST for Ranges and Exclusion Level C1

Investigate the GiST-backed exclusion lesson. First, try to reason about an
overlap rule without a GiST-backed exclusion constraint and explain why
PostgreSQL exclusion constraints require a supporting access method. Then pivot
to the read workload: run a range `&&` query, add the GiST index that supports
that operator, and prove the indexed range search is fast at scale.

Record the before and after plan and explain the maintenance tradeoff.
