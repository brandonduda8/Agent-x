import time


class GenesisRealityCollector:

    def __init__(self):

        self.system = "GENESIS REALITY COLLECTOR v1"

        self.data = {
            "jobs": [],
            "business_leads": [],
            "housing_resources": [],
            "completed_actions": []
        }


    def collect(self, category, item):

        if category not in self.data:
            return {
                "status": "UNKNOWN_CATEGORY",
                "category": category
            }

        self.data[category].append({
            "item": item,
            "timestamp": time.time()
        })

        return {
            "status": "COLLECTED",
            "category": category,
            "item": item
        }


    def status(self):

        return {
            "system": self.system,
            "status": "ONLINE",
            "data": self.data,
            "timestamp": time.time()
        }


reality_collector = GenesisRealityCollector()
