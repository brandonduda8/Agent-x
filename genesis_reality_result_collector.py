import time
import uuid

class RealityResultCollector:

    def __init__(self):
        self.results = []

    def record(self, category, agent, objective, status, result=None):
        item = {
            "id": f"result_{uuid.uuid4().hex[:8]}",
            "category": category,
            "agent": agent,
            "objective": objective,
            "status": status,
            "result": result,
            "timestamp": time.time()
        }

        self.results.append(item)

        print(item)
        return item

    def status(self):
        return {
            "system": "GENESIS REALITY RESULT COLLECTOR v1",
            "status": "ONLINE",
            "results": self.results,
            "count": len(self.results),
            "timestamp": time.time()
        }


collector = RealityResultCollector()
