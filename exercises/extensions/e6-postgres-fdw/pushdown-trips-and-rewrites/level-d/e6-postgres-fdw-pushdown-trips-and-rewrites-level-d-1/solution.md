# Solution

Identify the non-pushable function that keeps the aggregate local. Rewrite the filter or projection so the remote SQL can contain the grouped aggregate, then verify with EXPLAIN VERBOSE. The answer should name the original aggregate query that does not push down due to a non-pushable function and show the safer rewrite.
