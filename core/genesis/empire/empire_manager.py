import time
import uuid

from core.genesis.empire.company_portfolio import (
    company_portfolio
)

from core.genesis.empire.resource_allocator import (
    resource_allocator
)

from core.genesis.empire.growth_engine import (
    growth_engine
)


class GenesisEmpireManager:

    def __init__(self):

        self.system = (
            "GENESIS EMPIRE MANAGER v1"
        )


    def create_empire_cycle(
        self,
        objective,
        market
    ):

        print(
            "👑 Genesis Empire cycle started"
        )


        company = (
            company_portfolio.register_company(
                objective,
                market,
                "HIGH"
            )
        )


        growth = (
            growth_engine.evaluate(
                company
            )
        )


        resources = (
            resource_allocator.allocate(
                [
                    company
                ],
                [
                    "Sales Agent",
                    "Automation Agent",
                    "Coding Agent",
                    "Lead Generation Agent"
                ]
            )
        )


        result = {

            "id":
            "empire_cycle_" +
            uuid.uuid4().hex[:8],

            "company":
            company,

            "growth":
            growth,

            "resources":
            resources,

            "status":
            "ACTIVE",

            "timestamp":
            time.time()
        }


        print(
            "🏛️ Empire cycle complete"
        )


        return result


    def report(self):

        return {
            "system": self.system,
            "portfolio":
            company_portfolio.analyze_portfolio(),
            "timestamp": time.time()
        }


empire_manager = GenesisEmpireManager()
