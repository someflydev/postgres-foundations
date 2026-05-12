# No Restore Drills

Backups are only evidence of intent until they have been restored. A system that writes backup files but never restores them does not know whether the archive is complete, whether extensions exist on the target, whether permissions survive, or whether the application can start against the restored database.

This anti-pattern usually appears in teams with good intentions and vague confidence. They can name the backup schedule, but not the most recent restore timestamp, validation query, owner, duration, or failure discovered by the drill.

Prefer scheduled restore drills. Restore into a fresh target, install required extensions, run schema checks, run data validation queries, confirm application smoke tests, and record the measured RTO and RPO. Treat failures as useful findings, not paperwork.
