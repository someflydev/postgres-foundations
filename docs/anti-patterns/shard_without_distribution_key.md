# Anti-Pattern: Sharding Without a Distribution Key

Sharding before the workload has a proven distribution key turns Citus into accidental distributed complexity. The system pays for worker placement, cross-shard joins, distributed backups, and failover planning without earning locality.

Reject Citus when the proposal is performance insurance, a substitute for indexes, or an attempt to postpone schema and query design. A responsible Citus design names the tenant or entity key, lists the hot joins that remain co-located, identifies reference tables, and shows the queries that still need single-node PostgreSQL or another architecture.
