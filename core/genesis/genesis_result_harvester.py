import time


class GenesisResultHarvester:

    def __init__(self):
        self.results = {
            "income": [],
            "revenue": [],
            "housing": [],
            "execution": []
        }

    def record(self, category, item, agent):
        result = {
            "category": category,
            "item": item,
            "agent": agent,
            "status": "RECORDED",
            "timestamp": time.time()
        }

        if category in self.results:
            self.results[category].append(result)

        return result

    def status(self):
        return {
            "system": "GENESIS RESULT HARVESTER v1",
            "status": "ONLINE",
            "results": self.results,
            "timestamp": time.time()
        }


result_harvester = GenesisResultHarvester()
