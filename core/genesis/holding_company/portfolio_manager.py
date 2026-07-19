import time
import uuid


class PortfolioManager:

    def __init__(self):
        self.system = "GENESIS PORTFOLIO MANAGER v1"
        self.companies = []


    def register(self, company):

        record = {
            "id": "portfolio_" + uuid.uuid4().hex[:8],
            "company": company["name"],
            "market": company["market"],
            "status": "ACTIVE",
            "timestamp": time.time()
        }

        self.companies.append(record)

        print(
            f"🏢 Portfolio company registered: {company['name']}"
        )

        return record


    def analyze(self):

        return {
            "companies": len(self.companies),
            "active": len(self.companies),
            "timestamp": time.time()
        }


portfolio_manager = PortfolioManager()
