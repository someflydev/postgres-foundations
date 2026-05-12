# Vacuum Starvation by Long Transaction

Vacuum can only remove dead tuples that are no longer visible to any active snapshot. A long transaction, idle transaction, prepared transaction, or lagging replication slot can hold that visibility horizon back while ordinary writes keep creating dead rows.

The anti-pattern appears when bloat grows even though autovacuum is enabled. Operators tune vacuum more aggressively, but the real blocker is an old transaction or slot that keeps `xmin` in the past.

Prefer bounding transaction duration, keeping reporting work out of OLTP sessions, monitoring old snapshots, and alerting on replication slot lag. When bloat appears, identify the blocker before changing vacuum settings.
