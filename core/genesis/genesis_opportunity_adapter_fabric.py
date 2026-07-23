import time
import json
import os


class GenesisOpportunityAdapterFabric:

    def __init__(self):
        self.file = "data/genesis_opportunity_adapters.json"
        self.adapters = {}
        self.load()

    def load(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    data = json.load(f)

                for adapter in data:
                    self.adapters[adapter["name"]] = adapter

        except Exception:
            self.adapters = {}

    def save(self):
        os.makedirs("data", exist_ok=True)

        with open(self.file, "w") as f:
            json.dump(
                list(self.adapters.values()),
                f,
                indent=2
            )

    def register(self, name, category, source_type):

        self.adapters[name] = {
            "name": name,
            "category": category,
            "source_type": source_type,
            "status": "CONNECTED",
            "timestamp": time.time()
        }

        self.save()

        return self.adapters[name]


    def status(self):
        return {
            "system": "GENESIS EXTERNAL OPPORTUNITY ADAPTER FABRIC v2",
            "status": "ONLINE",
            "adapters": list(self.adapters.values()),
            "count": len(self.adapters),
            "timestamp": time.time()
        }


opportunity_adapter_fabric = GenesisOpportunityAdapterFabric()
