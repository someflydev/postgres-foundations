"""Print deterministic Phase 8 document corpus CSV rows."""

from __future__ import annotations

import csv
import sys
from collections.abc import Iterator

ROW_COUNT = 5000

TOPICS = [
    "postgres indexing",
    "backup restore",
    "vacuum maintenance",
    "query planning",
    "tenant isolation",
    "jsonb boundaries",
    "transaction safety",
    "search ranking",
    "schema migration",
    "observability metrics",
    "connection pooling",
    "incident review",
]
ACTIONS = ["guide", "checklist", "runbook", "field note", "design review", "operator memo"]
AUTHORS = ["Platform Team", "Support Team", "Data Team", "Reliability Team", "Education Team"]
TAG_SETS = [
    "{postgres,indexing,operations}",
    "{backup,restore,operations}",
    "{vacuum,maintenance,performance}",
    "{query,planning,indexing}",
    "{tenant,isolation,saas}",
    "{jsonb,modeling,boundaries}",
    "{transaction,correctness,locks}",
    "{search,ranking,documents}",
    "{migration,schema,safety}",
    "{observability,metrics,plans}",
    "{pooling,connections,operations}",
    "{incident,review,repair}",
]
CATEGORIES = ["operations", "performance", "modeling", "correctness", "search"]


def iter_rows(row_count: int = ROW_COUNT) -> Iterator[dict[str, str]]:
    for index in range(1, row_count + 1):
        topic_index = (index - 1) % len(TOPICS)
        topic = TOPICS[topic_index]
        action = ACTIONS[(index * 7) % len(ACTIONS)]
        title = f"{topic.title()} {action.title()} {index:04d}"
        body = (
            f"This document explains {topic} for PostgreSQL teams. "
            "Paragraph one describes the workload signal, the failure mode, "
            "and the operator question.\n\n"
            f"Paragraph two gives a concrete SQL practice for {topic}, including "
            "measurement, review, and rollback notes. Postgres indexing examples "
            "appear throughout the corpus so lexical search has realistic repeated terms.\n\n"
            "Paragraph three records follow-up checks for maintainers, including "
            "explain plans, ranking expectations, and portability concerns before "
            "adding external systems."
        )
        yield {
            "id": f"00000000-0000-0000-0000-{index:012d}",
            "title": title,
            "body": body,
            "published_at": f"2026-04-{((index - 1) % 28) + 1:02d} 12:00:00+00",
            "author": AUTHORS[index % len(AUTHORS)],
            "tags": TAG_SETS[topic_index],
            "category_slug": CATEGORIES[index % len(CATEGORIES)],
        }


def main() -> None:
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["id", "title", "body", "published_at", "author", "tags", "category_slug"],
    )
    writer.writeheader()
    writer.writerows(iter_rows())


if __name__ == "__main__":
    main()
