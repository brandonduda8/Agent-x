import time
import json
import os


class GenesisRealityResultsEngine:

    def __init__(self):
        self.file = "data/genesis_reality_results.json"
        self.results = {
            "income": [],
            "revenue": [],
            "housing": [],
            "execution": []
        }
        self.load()


    def load(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    self.results = json.load(f)
        except Exception:
            pass


    def save(self):
        os.makedirs("data", exist_ok=True)

        with open(self.file, "w") as f:
            json.dump(
                self.results,
                f,
                indent=2
            )


    def record(self, category, action, agent, status="READY"):

        item = {
            "category": category,
            "action": action,
            "agent": agent,
            "status": status,
            "timestamp": time.time()
        }

        if category not in self.results:
            self.results[category] = []

        self.results[category].append(item)

        self.save()

        return item


    def status(self):

        return {
            "system": "GENESIS REALITY RESULTS ENGINE v1",
            "status": "ONLINE",
            "results": self.results,
            "timestamp": time.time()
        }


results_engine = GenesisRealityResultsEngine()
