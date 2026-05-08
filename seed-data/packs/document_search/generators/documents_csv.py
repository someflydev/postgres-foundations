"""Print deterministic document CSV rows."""

import csv
import random
import sys


def main() -> None:
    random.seed(19009)
    writer = csv.writer(sys.stdout)
    writer.writerow(["slug", "title", "body", "status"])
    topics = ["backup", "restore", "index", "vacuum", "tenant", "jsonb"]
    verbs = ["check", "review", "repair", "explain"]
    for index in range(20):
        topic = random.choice(topics)
        verb = random.choice(verbs)
        slug = f"{topic}-{verb}-{index:02d}"
        title = f"{topic.title()} {verb.title()} {index:02d}"
        body = f"Document {index} explains how to {verb} a {topic} workflow in PostgreSQL."
        writer.writerow([slug, title, body, "published"])


if __name__ == "__main__":
    main()
