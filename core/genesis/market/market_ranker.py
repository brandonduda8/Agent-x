import time
import uuid


class MarketRanker:

    def __init__(self):
        self.system = "GENESIS MARKET RANKER v1"

    def rank(self, opportunities):

        ranked = sorted(
            opportunities,
            key=lambda x: x["score"],
            reverse=True
        )

        result = {
            "id": "ranking_" + uuid.uuid4().hex[:8],
            "ranking": ranked,
            "timestamp": time.time()
        }

        print("📈 Markets ranked")

        return result


market_ranker = MarketRanker()
