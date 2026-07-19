import time
import uuid

from core.genesis.holding_company.portfolio_manager import (
    portfolio_manager
)

from core.genesis.holding_company.capital_allocator import (
    capital_allocator
)

from core.genesis.holding_company.growth_engine import (
    growth_engine
)


class HoldingCompany:

    def __init__(self):

        self.system = (
            "GENESIS AUTONOMOUS HOLDING COMPANY v1"
        )


        self.cycles = []


    def operate(self, company):


        print(
            "👑 Genesis Holding Company activated"
        )


        registered = portfolio_manager.register(
            company
        )


        portfolio = portfolio_manager.analyze()


        capital = capital_allocator.allocate(
            portfolio_manager.companies
        )


        growth = growth_engine.decide(
            portfolio
        )


        result = {

            "id":
            "holding_cycle_" +
            uuid.uuid4().hex[:8],

            "company":
            registered,

            "portfolio":
            portfolio,

            "capital":
            capital,

            "growth":
            growth,

            "status":
            "ACTIVE",

            "timestamp":
            time.time()
        }


        self.cycles.append(result)


        print(
            "🏛 Holding company cycle complete"
        )


        return result



holding_company = HoldingCompany()
