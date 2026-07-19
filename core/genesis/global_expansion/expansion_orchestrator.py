import uuid
import time

from .market_expansion_engine import (
    market_expansion_engine
)

from .geographic_intelligence import (
    geographic_intelligence
)

from .expansion_strategy_engine import (
    expansion_strategy_engine
)


class ExpansionOrchestrator:

    def __init__(self):

        self.system = (
            "GENESIS GLOBAL EXPANSION ORCHESTRATOR v1"
        )

        self.cycles = []


    def run(self, objective):

        print(
            "🌎 Genesis global expansion cycle started"
        )

        market_scan = (
            market_expansion_engine.scan(objective)
        )

        ranked = sorted(
            market_scan["markets"],
            key=lambda x: x["score"],
            reverse=True
        )

        primary_market = ranked[0]

        strategy = (
            expansion_strategy_engine.decide(
                primary_market
            )
        )

        geography = (
            geographic_intelligence.analyze(
                primary_market["market"]
            )
        )


        result = {

            "id":
            "global_expansion_" +
            uuid.uuid4().hex[:8],

            "objective":
            objective,

            "market":
            primary_market,

            "strategy":
            strategy,

            "geography":
            geography,

            "status":
            "READY",

            "timestamp":
            time.time()
        }


        self.cycles.append(result)

        print(
            "🚀 Global expansion strategy created"
        )

        return result


    def report(self):

        return {

            "system":
            self.system,

            "cycles":
            len(self.cycles),

            "timestamp":
            time.time()
        }


expansion_orchestrator = ExpansionOrchestrator()
