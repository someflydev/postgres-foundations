"""Generate deterministic phase 7a ecommerce CSV fixtures under tmp/."""

from __future__ import annotations

import csv
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

PRODUCT_COUNT = 5_200
CUSTOMER_COUNT = 12_000
ORDER_COUNT = 205_000
ITEMS_PER_ORDER = 5
SEED = 72001


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def write_csv(path: Path, header: tuple[str, ...], rows: list[tuple[object, ...]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    random.seed(SEED)
    output_dir = repo_root() / "tmp" / "generated-seed-data" / "ecommerce" / "phase-07a"
    base_time = datetime(2025, 1, 1, tzinfo=UTC)

    products = [
        (
            f"P7A-SKU-{idx:05d}",
            f"Phase 7A Product {idx:05d}",
            f"{9 + (idx % 190) + ((idx % 4) * 0.25):.2f}",
            25 + (idx % 500),
            (base_time - timedelta(days=idx % 365)).isoformat(),
        )
        for idx in range(1, PRODUCT_COUNT + 1)
    ]
    write_csv(
        output_dir / "products.csv",
        ("sku", "name", "price", "stock_on_hand", "created_at"),
        products,
    )

    customers = [
        (
            f"phase7a-customer-{idx:05d}@example.com",
            f"Phase 7A Customer {idx:05d}",
            (base_time + timedelta(minutes=idx)).isoformat(),
        )
        for idx in range(1, CUSTOMER_COUNT + 1)
    ]
    write_csv(output_dir / "customers.csv", ("email", "full_name", "created_at"), customers)

    statuses = ("placed", "paid", "shipped")
    orders: list[tuple[object, ...]] = []
    order_items: list[tuple[object, ...]] = []
    for order_idx in range(1, ORDER_COUNT + 1):
        customer_idx = ((order_idx * 37) % CUSTOMER_COUNT) + 1
        placed_at = base_time + timedelta(minutes=order_idx * 7)
        status = statuses[order_idx % len(statuses)]
        order_number = f"P7A-{order_idx:07d}"
        total = 0.0
        item_rows: list[tuple[object, ...]] = []
        for line_idx in range(ITEMS_PER_ORDER):
            product_idx = ((order_idx * 17) + (line_idx * 97)) % PRODUCT_COUNT + 1
            quantity = 1 + ((order_idx + line_idx) % 3)
            unit_price = 9 + (product_idx % 190) + ((product_idx % 4) * 0.25)
            total += quantity * unit_price
            item_rows.append(
                (
                    order_number,
                    f"P7A-SKU-{product_idx:05d}",
                    quantity,
                    f"{unit_price:.2f}",
                    (placed_at + timedelta(seconds=line_idx)).isoformat(),
                )
            )
        orders.append(
            (
                f"phase7a-customer-{customer_idx:05d}@example.com",
                order_number,
                status,
                f"{total:.2f}",
                placed_at.isoformat(),
            )
        )
        order_items.extend(item_rows)

    write_csv(
        output_dir / "orders.csv",
        ("customer_email", "order_number", "status", "total_amount", "placed_at"),
        orders,
    )
    write_csv(
        output_dir / "order_items.csv",
        ("order_number", "sku", "quantity", "unit_price", "created_at"),
        order_items,
    )
    print(output_dir)


if __name__ == "__main__":
    main()
