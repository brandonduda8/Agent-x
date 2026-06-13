import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "../stripe-catalog/config.json"


def load_catalog():
    with open(CATALOG_PATH, "r") as f:
        return json.load(f)


def save_catalog(catalog):
    with open(CATALOG_PATH, "w") as f:
        json.dump(catalog, f, indent=2)


def generate_product(product_type, name, price_cents=None, description=None):
    return {
        "type": product_type,
        "name": name,
        "price_cents": price_cents,
        "description": description
    }


def register_in_catalog(product):
    catalog = load_catalog()

    if "products" not in catalog:
        catalog["products"] = []

    catalog["products"].append(product)

    save_catalog(catalog)


def main():
    if len(sys.argv) < 3:
        print("Usage: product-orchestrator.py <type> <name> [price_cents] [description]")
        return

    product_type = sys.argv[1]
    name = sys.argv[2]
    price_cents = int(sys.argv[3]) if len(sys.argv) > 3 else None
    description = sys.argv[4] if len(sys.argv) > 4 else None

    product = generate_product(product_type, name, price_cents, description)

    print(f"[orchestrator] generating {product_type}: {name}")

    register_in_catalog(product)

    print("[orchestrator] product saved to catalog")


if __name__ == "__main__":
    main()
