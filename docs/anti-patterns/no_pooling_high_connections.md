# No Pooling With High Connections

PostgreSQL connections are useful but not free. Each backend consumes memory and scheduling attention, so raising `max_connections` to match every web worker or job process is usually a sign that concurrency is not being controlled.

This anti-pattern appears when autoscaling application fleets create hundreds or thousands of mostly idle sessions. The database may look connection-bound before it is CPU-bound, and transaction latency can worsen because too much work is admitted at once.

Prefer bounded application pools and PgBouncer when connection churn is a measured problem. Choose the pool mode deliberately, test prepared statements and session settings, and document how failover updates pool targets.
