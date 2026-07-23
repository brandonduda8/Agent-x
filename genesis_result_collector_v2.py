import time
import uuid


class GenesisResultCollector:

    def __init__(self):
        self.results = []


    def collect(self, execution, output):

        result = {
            "result_id": "result_" + str(uuid.uuid4())[:8],
            "execution_id": execution["execution_id"],
            "mission_id": execution["mission_id"],
            "agent": execution["agent"],
            "category": execution["category"],
            "objective": execution["objective"],
            "output": output,
            "status": "VERIFIED",
            "timestamp": time.time()
        }

        self.results.append(result)

        return result


    def summarize(self):

        summary = {
            "income": [],
            "revenue": [],
            "housing": [],
            "development": []
        }

        for result in self.results:
            category = result["category"]

            if category in summary:
                summary[category].append(result)


        return {
            "system": "GENESIS RESULT COLLECTOR v2",
            "status": "ONLINE",
            "results": summary,
            "total_results": len(self.results),
            "timestamp": time.time()
        }


    def status(self):

        return {
            "system": "GENESIS RESULT COLLECTOR v2",
            "status": "ONLINE",
            "results": self.results,
            "count": len(self.results),
            "timestamp": time.time()
        }


result_collector = GenesisResultCollector()
