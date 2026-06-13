import json
from pathlib import Path
from datetime import datetime


class RevenueEngine:

    def __init__(self, path="memory/revenue.json"):

        self.file = Path(path)
        self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():
            self.file.write_text("[]")

    # -------------------------
    # LOAD DATA
    # -------------------------
    def load(self):

        return json.loads(self.file.read_text())

    # -------------------------
    # SAVE DATA
    # -------------------------
    def save(self, data):

        self.file.write_text(json.dumps(data, indent=2))

    # -------------------------
    # ADD REVENUE EVENT
    # -------------------------
    def add(self, source, amount, meta=None):

        data = self.load()

        data.append({
            "source": source,
            "amount": amount,
            "meta": meta or {},
            "time": datetime.utcnow().isoformat()
        })

        self.save(data)

    # -------------------------
    # TOTAL REVENUE
    # -------------------------
    def total(self):

        return sum(x["amount"] for x in self.load())

    # -------------------------
    # SOURCE BREAKDOWN
    # -------------------------
    def breakdown(self):

        data = self.load()

        result = {}

        for item in data:

            src = item["source"]

            result[src] = result.get(src, 0) + item["amount"]

        return result
