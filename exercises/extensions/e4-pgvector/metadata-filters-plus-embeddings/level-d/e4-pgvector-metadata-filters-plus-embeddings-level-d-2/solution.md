# Solution

Diagnose the recall loss as a query-shape problem. The approximate vector step returns neighbors first, then a metadata predicate discards many of them. Precompute the metadata slice with ordinary indexes, increase candidate count, or run separate filtered probes before ranking. Verify with recall at k against an exact distance query on the same filtered set.
