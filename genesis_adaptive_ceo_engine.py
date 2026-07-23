import time


class GenesisAdaptiveCEOEngine:

    def __init__(self):
        self.decisions = []


    def evaluate(self, metrics):

        decisions = []

        if metrics["income_progress"] < 5:
            decisions.append({
                "area":"income",
                "decision":"INCREASE_JOB_OUTPUT",
                "reason":"Income progress below target"
            })


        if metrics["revenue_progress"] < 5:
            decisions.append({
                "area":"revenue",
                "decision":"INCREASE_BUSINESS_OUTREACH",
                "reason":"Revenue pipeline needs growth"
            })


        if metrics["housing_progress"] < 5:
            decisions.append({
                "area":"housing",
                "decision":"PRIORITIZE_STABILITY",
                "reason":"Housing progress needs attention"
            })


        if metrics["development_progress"] < 3:
            decisions.append({
                "area":"development",
                "decision":"IMPROVE_TECHNICAL_CAPABILITY",
                "reason":"Development growth required"
            })


        self.decisions.extend(decisions)

        return {
            "system":"GENESIS ADAPTIVE CEO ENGINE v1",
            "status":"ONLINE",
            "decisions":decisions,
            "timestamp":time.time()
        }


    def status(self):

        return {
            "system":"GENESIS ADAPTIVE CEO ENGINE v1",
            "decisions":self.decisions,
            "timestamp":time.time()
        }


ceo_engine = GenesisAdaptiveCEOEngine()
