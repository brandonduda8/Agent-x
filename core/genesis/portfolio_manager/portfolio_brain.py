import uuid
import time


from core.genesis.portfolio_manager.portfolio_registry import (
    portfolio_registry
)

from core.genesis.portfolio_manager.company_ranker import (
    company_ranker
)

from core.genesis.portfolio_manager.capital_distribution import (
    capital_distribution
)

from core.genesis.portfolio_manager.acquisition_manager import (
    acquisition_manager
)


class PortfolioBrain:

    def __init__(self):
        self.cycles = []


    def execute(self):

        print(
            "🌐 Portfolio Manager activated"
        )

        company = portfolio_registry.register(
            "Healthcare AI Automation Company",
            "Healthcare AI"
        )

        ranking = company_ranker.rank(
            portfolio_registry.companies
        )

        capital = capital_distribution.allocate(
            portfolio_registry.companies
        )

        acquisitions = acquisition_manager.analyze()


        cycle = {
            "id": f"portfolio_{uuid.uuid4().hex[:8]}",
            "companies": portfolio_registry.companies,
            "ranking": ranking,
            "capital": capital,
            "acquisitions": acquisitions,
            "status": "COMPLETE",
            "timestamp": time.time()
        }


        self.cycles.append(cycle)


        print(
            "🚀 Portfolio optimization complete"
        )

        return cycle


portfolio_brain = PortfolioBrain()
