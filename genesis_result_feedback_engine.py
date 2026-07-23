import time


class GenesisResultFeedbackEngine:

    def __init__(self):
        self.results = []


    def submit_result(self, mission_id, agent, category, result):

        record = {
            "mission_id": mission_id,
            "agent": agent,
            "category": category,
            "result": result,
            "verified": True,
            "timestamp": time.time()
        }

        self.results.append(record)

        return record


    def analyze(self):

        metrics = {
            "income_progress": 0,
            "revenue_progress": 0,
            "housing_progress": 0,
            "development_progress": 0
        }

        for result in self.results:

            if result["category"] == "income":
                metrics["income_progress"] += 1

            elif result["category"] == "revenue":
                metrics["revenue_progress"] += 1

            elif result["category"] == "housing":
                metrics["housing_progress"] += 1

            elif result["category"] == "development":
                metrics["development_progress"] += 1


        return {
            "system":
                "GENESIS RESULT FEEDBACK ENGINE v1",
            "metrics":
                metrics,
            "timestamp":
                time.time()
        }


feedback_engine = GenesisResultFeedbackEngine()
