#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

BASE = Path.home() / "agent-x" / "products"
CATALOG = BASE / "catalog" / "catalog.json"

products = [
    ("ebook", "$14.99 AI Automation Playbook", 1499, "Best-selling automation guide"),
    ("ebook", "$9.99 Side Hustle OS", 999, "Simple income system"),
    ("template-pack", "$19.99 Notion Templates", 1999, "Business dashboards"),
    ("swipe-file", "$7.99 Cold Email Swipes", 799, "High reply subject lines"),
]

result = []

for p_type, name, price, desc in products:
    args = [sys.executable, str(BASE / "product-factory.py"), p_type, name, str(price), desc]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode == 0:
        product = json.loads(r.stdout)
        result.append({"name": name, "ok": True, "productId": product.get("productId")})
    else:
        result.append({"name": name, "ok": False, "error": (r.stderr or r.stdout).strip()[:120]})

print(json.dumps({"batchSize": len(result), "products": result}, indent=2))