import time
import uuid


class OpportunityExecutionEngine:

    def __init__(self):
        self.opportunities = []


    def add_opportunity(self, category, source, title, value):

        item = {
            "id": "opp_" + uuid.uuid4().hex[:8],
            "category": category,
            "source": source,
            "title": title,
            "value": value,
            "priority": self.score(value),
            "status": "DISCOVERED",
            "timestamp": time.time()
        }

        self.opportunities.append(item)

        return item


    def score(self, value):

        score = 0

        if "immediate" in value.lower():
            score += 3

        if "remote" in value.lower():
            score += 2

        if "income" in value.lower():
            score += 2

        return score


    def status(self):

        return {
            "system": "GENESIS OPPORTUNITY EXECUTION ENGINE v1",
            "status": "ONLINE",
            "opportunities": self.opportunities,
            "count": len(self.opportunities),
            "timestamp": time.time()
        }


opportunity_engine = OpportunityExecutionEngine()
