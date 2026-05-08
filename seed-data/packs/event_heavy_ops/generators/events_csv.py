"""Print deterministic event CSV rows."""

import csv
import random
import sys
from datetime import UTC, datetime, timedelta


def main() -> None:
    random.seed(9042)
    writer = csv.writer(sys.stdout)
    writer.writerow(["event_uuid", "source_key", "event_type", "occurred_at", "payload"])
    base = datetime(2026, 3, 1, 12, 0, tzinfo=UTC)
    sources = ["checkout-prod", "billing-prod", "catalog-prod"]
    event_types = ["order_placed", "payment_captured", "stock_adjusted", "job_retried"]
    for index in range(20):
        source = random.choice(sources)
        event_type = random.choice(event_types)
        occurred_at = base + timedelta(seconds=index * random.randint(20, 90))
        payload = f'{{"sequence": {index}, "source": "{source}"}}'
        writer.writerow(
            [
                f"90000000-0000-0000-0000-{index:012d}",
                source,
                event_type,
                occurred_at.isoformat(),
                payload,
            ]
        )


if __name__ == "__main__":
    main()
