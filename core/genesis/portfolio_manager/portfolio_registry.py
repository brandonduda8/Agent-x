import uuid
import time


class PortfolioRegistry:

    def __init__(self):
        self.companies = []


    def register(self, company, market):

        entry = {
            "id": f"company_{uuid.uuid4().hex[:8]}",
            "company": company,
            "market": market,
            "status": "ACTIVE",
            "timestamp": time.time()
        }

        self.companies.append(entry)

        print(
            f"🏢 Company registered: {company}"
        )

        return entry


portfolio_registry = PortfolioRegistry()
