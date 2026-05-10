# GIN for JSONB and Arrays Level C1

Run a JSONB containment query on events.payload, then add a GIN jsonb_path_ops index and compare the Seq Scan versus index-backed plan diff with pgfound lab explain.

Record the before and after plan and explain the maintenance tradeoff.
