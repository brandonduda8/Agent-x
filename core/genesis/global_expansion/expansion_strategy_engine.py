import uuid
import time


class ExpansionStrategyEngine:

    def __init__(self):
        self.system = "GENESIS EXPANSION STRATEGY ENGINE v1"

    def decide(self, market):

        if market["score"] >= 90:
            decision = "SCALE"

        elif market["score"] >= 85:
            decision = "ACQUIRE"

        else:
            decision = "BUILD"

        return {
            "id": "strategy_" + uuid.uuid4().hex[:8],
            "market": market["market"],
            "score": market["score"],
            "decision": decision,
            "timestamp": time.time()
        }


expansion_strategy_engine = ExpansionStrategyEngine()
