"""Inventory management system with secure and clean code practices."""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Global in-memory inventory
stock_data: Dict[str, int] = {}


def add_item(item: str, qty: int, logs: Optional[List[str]] = None) -> None:
    """Add an item with the given quantity to the stock."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not item:
        raise ValueError("item must be a non-empty string")

    if not isinstance(qty, int) or qty < 0:
        raise ValueError("qty must be a non-negative integer")

    if qty == 0:
        logging.info("add_item: zero quantity received for %s — no change", item)
        return

    previous = stock_data.get(item, 0)
    stock_data[item] = previous + qty
    log_entry = (
        f"{datetime.now().isoformat()}: Added {qty} of {item} "
        f"(was {previous}, now {stock_data[item]})"
    )
    logs.append(log_entry)
    logging.info(log_entry)


def remove_item(item: str, qty: int) -> None:
    """Remove a specific quantity of an item from the inventory."""
    if not isinstance(item, str) or not item:
        raise ValueError("item must be a non-empty string")

    if not isinstance(qty, int) or qty <= 0:
        raise ValueError("qty must be a positive integer")

    if item not in stock_data:
        logging.warning("remove_item: item '%s' not in stock", item)
        raise KeyError(f"item '{item}' not found")

    current = stock_data[item]
    if qty > current:
        logging.warning(
            "remove_item: requested removal %d greater than current %d for %s",
            qty,
            current,
            item,
        )
        raise ValueError("cannot remove more than current stock")

    new_qty = current - qty
    if new_qty == 0:
        del stock_data[item]
        logging.info("%s: Removed %d of %s — item removed", datetime.now().isoformat(), qty, item)
    else:
        stock_data[item] = new_qty
        logging.info("%s: Removed %d of %s — now %d left", datetime.now().isoformat(), qty, item, new_qty)


def get_qty(item: str) -> int:
    """Return the quantity of a specific item."""
    if not isinstance(item, str) or not item:
        raise ValueError("item must be a non-empty string")

    if item not in stock_data:
        logging.error("get_qty: item '%s' not found", item)
        raise KeyError(f"item '{item}' not found")

    return stock_data[item]


def load_data(file_path: str = "inventory.json") -> Dict[str, int]:
    """Load inventory data from JSON file and return it."""
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        logging.warning("File %s not found — starting empty inventory", file_path)
        return {}
    except json.JSONDecodeError as exc:
        logging.error("Invalid JSON in %s: %s", file_path, exc)
        raise

    if not isinstance(data, dict):
        raise ValueError("inventory file must contain an object mapping item->qty")

    validated: Dict[str, int] = {}
    for k, v in data.items():
        if isinstance(k, str) and isinstance(v, int):
            validated[k] = v
        else:
            logging.warning("Skipping invalid entry: %r -> %r", k, v)

    logging.info("Loaded %d items from %s", len(validated), file_path)
    return validated


def save_data(file_path: str = "inventory.json") -> None:
    """Save inventory data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as fh:
        json.dump(stock_data, fh, indent=2)
    logging.info("Saved %d items to %s", len(stock_data), file_path)


def print_data() -> None:
    """Print all items and quantities."""
    if not stock_data:
        print("Inventory is empty.")
        return

    print("\n=== Inventory Report ===")
    for name, qty in sorted(stock_data.items()):
        print(f"{name} -> {qty}")


def check_low_items(threshold: int = 5) -> List[str]:
    """Return list of items whose quantity is below threshold."""
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError("threshold must be a non-negative integer")

    return [name for name, qty in stock_data.items() if qty < threshold]


def _demo_operations() -> None:
    """Run sample operations to demonstrate the inventory system."""
    logs: List[str] = []

    try:
        add_item("apple", 10, logs)
        add_item("banana", 3, logs)
        remove_item("banana", 1)
        print_data()
        print("Low items:", check_low_items())
        logging.info("Operation logs: %s", logs)
    except (ValueError, KeyError) as exc:
        logging.error("Demo operation error: %s", exc)


if __name__ == "__main__":
    # Safe runtime entrypoint
    stock_data = load_data()
    _demo_operations()
    save_data()
