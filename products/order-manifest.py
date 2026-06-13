#!/usr/bin/env python3
"""Agent X Order Manifest Generator
Creates order records for manual sales channels.
"""
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

BASE = Path.home() / "agent-x" / "products"
STATE = BASE / "state"
DELIVERABLES = BASE / "deliverables"
ORDERS_FILE = STATE / "orders.json"

def create_order(product_id, buyer_email=None, channel="manual"):
    now = datetime.now(timezone.utc).isoformat()
    order_id = f"order_{int(time.time()*1000)}_{channel}"

    order = {
        "id": order_id,
        "productId": product_id,
        "buyerEmail": buyer_email or "pending",
        "channel": channel,
        "status": "paid",
        "paidAt": now,
        "deliveredAt": None,
        "downloadUrl": f"http://localhost:4000/ingest?order={order_id}"
    }

    # Save order
    orders = []
    if ORDERS_FILE.exists():
        try:
            orders = json.loads(ORDERS_FILE.read_text())
        except Exception:
            orders = []
    orders.append(order)
    ORDERS_FILE.write_text(json.dumps(orders, indent=2), encoding="utf-8")

    return order

def main():
    if len(sys.argv) < 2:
        print("Usage: order-manifest.py <product_id> [buyer_email] [channel]")
        print("Channels: manual, paypal, venmo, cashapp-link, social-dm")
        raise SystemExit(1)

    product_id = sys.argv[1]
    buyer_email = sys.argv[2] if len(sys.argv) > 2 else None
    channel = sys.argv[3] if len(sys.argv) > 3 else "manual"

    order = create_order(product_id, buyer_email, channel)

    print(json.dumps({
        "ok": True,
        "orderId": order["id"],
        "productId": order["productId"],
        "downloadUrl": order["downloadUrl"],
        "shareText": f"Thanks for your order! Download: {order['downloadUrl']}"
    }, indent=2))

if __name__ == "__main__":
    main()
