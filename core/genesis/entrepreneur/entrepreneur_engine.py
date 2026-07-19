import time
import uuid

from core.genesis.market.market_scanner import market_scanner
from core.genesis.market.opportunity_detector import opportunity_detector
from core.genesis.market.market_ranker import market_ranker
from core.genesis.market.business_generator import business_generator


class GenesisEntrepreneurEngine:

    def __init__(self):
        self.system = "GENESIS AUTONOMOUS ENTREPRENEUR ENGINE v1"
        self.ventures = []

    def discover_opportunity(self):

        print("🔎 Discovering business opportunities")

        scan = market_scanner.scan()

        opportunities = []

        for market in scan["markets"]:
            opportunities.append(
                opportunity_detector.evaluate(market)
            )

        ranking = market_ranker.rank(opportunities)

        return ranking["ranking"][0]


    def create_venture(self):

        print("🧬 Entrepreneur cycle started")

        opportunity = self.discover_opportunity()

        print(
            f"🎯 Selected opportunity: {opportunity['market']}"
        )

        company = business_generator.create(
            opportunity
        )

        venture = {
            "id": "venture_" + uuid.uuid4().hex[:8],
            "opportunity": opportunity,
            "company": company,
            "status": "LAUNCHED",
            "timestamp": time.time()
        }

        self.ventures.append(venture)

        print(
            f"🚀 Venture launched: {company['name']}"
        )

        return venture


    def report(self):

        return {
            "system": self.system,
            "ventures": len(self.ventures),
            "timestamp": time.time()
        }


entrepreneur_engine = GenesisEntrepreneurEngine()
