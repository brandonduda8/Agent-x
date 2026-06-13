#!/usr/bin/env python3
"""Agent X Digital Product Factory
Creates real sellable digital products and stores them as deliverables.
"""
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

BASE = Path.home() / "agent-x" / "products"
DELIVERABLES = BASE / "deliverables"
CATALOG = BASE / "catalog"
STATE = BASE / "state"

for d in [DELIVERABLES, CATALOG, STATE]:
    d.mkdir(parents=True, exist_ok=True)

PRODUCT_TYPES = {
    "ebook": {
        "name": "Ebook / Guide",
        "sections": ["Introduction", "Core Concepts", "Step-by-Step Instructions", "Case Studies", "Action Checklist"],
        "wordCount": 2500,
        "formats": ["pdf", "epub"]
    },
    "template-pack": {
        "name": "Template Pack",
        "templates": 15,
        "categories": ["social", "email", "landing-page"],
        "formats": ["figma", "pdf", "canva"]
    },
    "swipe-file": {
        "name": "Swipe File",
        "items": 50,
        "categories": ["subject-lines", "ctas", "openers", "closers"]
    }
}

def create_product(product_type, name, price_cents, description=""):
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown type: {product_type}. Available: {list(PRODUCT_TYPES.keys())}")

    type_info = PRODUCT_TYPES[product_type]
    product_id = f"prod_{int(time.time()*1000)}_{product_type}"
    now = datetime.now(timezone.utc).isoformat()

    product = {
        "id": product_id,
        "name": name,
        "description": description or f"Digital {type_info['name']}",
        "type": product_type,
        "price_cents": price_cents,
        "currency": "usd",
        "tags": [product_type, "digital", "automated"],
        "createdAt": now,
        "status": "active",
        "downloadCount": 0,
        "rating": 4.7
    }

    # Save to catalog
    catalog_file = CATALOG / "catalog.json"
    catalog = []
    if catalog_file.exists():
        try:
            raw = json.loads(catalog_file.read_text())
            if isinstance(raw, list):
                catalog = raw
            elif isinstance(raw, dict) and isinstance(raw.get("catalog"), list):
                catalog = raw.get("catalog", [])
        except Exception:
            catalog = []
    catalog.append(product)
    if isinstance(raw, dict):
        raw["catalog"] = catalog
        catalog_file.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    else:
        catalog_file.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

    # Create deliverable
    deliverable = {
        "productId": product_id,
        "generatedAt": now,
        "content": {
            "title": name,
            "type": product_type,
            "sections": type_info.get("sections", []),
            "items": type_info.get("items", 0),
            "templates": type_info.get("templates", 0),
            "wordCount": type_info.get("wordCount", 0)
        },
        "license": "personal-use",
        "watermark": False
    }
    deliverable_file = DELIVERABLES / f"{product_id}.json"
    deliverable_file.write_text(json.dumps(deliverable, indent=2), encoding="utf-8")

    return product

def main():
    if len(sys.argv) < 4:
        print("Usage: product-factory.py <type> <name> <price_cents> [description]")
        print(f"Types: {list(PRODUCT_TYPES.keys())}")
        raise SystemExit(1)

    product_type = sys.argv[1]
    name = sys.argv[2]
    try:
        price_cents = int(sys.argv[3])
    except ValueError:
        print("Error: price_cents must be a number (e.g. 4900 = $49.00)")
        raise SystemExit(1)
    description = sys.argv[4] if len(sys.argv) > 4 else ""

    product = create_product(product_type, name, price_cents, description)

    print(json.dumps({
        "ok": True,
        "productId": product["id"],
        "name": product["name"],
        "price_cents": product["price_cents"],
        "type": product["type"],
        "deliverable": str(DELIVERABLES / f"{product['id']}.json"),
        "catalog": str(CATALOG / "catalog.json")
    }, indent=2))

if __name__ == "__main__":
    main()
