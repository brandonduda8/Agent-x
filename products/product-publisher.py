#!/usr/bin/env python3
"""Agent X Product Publisher
Auto-generates products and delivers them to webhook listener.
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

BASE = Path.home() / "agent-x" / "products"
SINK_URL = "http://localhost:4000/ingest"

FACTORY = BASE / "product-factory.py"
DELIVERABLES = BASE / "deliverables"

def run_factory(product_type, name, price_cents, description=""):
    args = [sys.executable, str(FACTORY), product_type, name, str(price_cents), description]
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

def deliver_to_sink(product, channel="auto-publish"):
    data = json.dumps({
        "source": "agent-x-products",
        "channel": channel,
        "ts": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        "product": product
    }).encode()

    req = urllib.request.Request(
        SINK_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())

def main():
    if len(sys.argv) < 4:
        print("Usage: product-publisher.py <type> <name> <price_cents> [description] [channel]")
        print("Types: ebook, template-pack, swipe-file")
        print("Channel: manual, paypal, venmo, cashapp-link, social-dm")
        raise SystemExit(1)

    product_type = sys.argv[1]
    name = sys.argv[2]
    price_cents = int(sys.argv[3])
    description = sys.argv[4] if len(sys.argv) > 4 else ""
    channel = sys.argv[5] if len(sys.argv) > 5 else "manual"

    print(f"[publisher] creating {product_type}: {name}", flush=True)

    # Generate product
    product = run_factory(product_type, name, price_cents, description)

    # Deliver to webhook listener
    receipt = deliver_to_sink(product, channel)

    print(json.dumps({
        "ok": True,
        "productId": product["productId"],
        "name": product["name"],
        "price_cents": product["price_cents"],
        "delivery": receipt,
        "download": product["deliverable"]
    }, indent=2))

if __name__ == "__main__":
    main()
