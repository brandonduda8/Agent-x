import time
import uuid


class CompanyPortfolio:

    def __init__(self):
        self.system = "GENESIS COMPANY PORTFOLIO v1"
        self.companies = []


    def register_company(
        self,
        name,
        market,
        potential
    ):

        company = {
            "id": "company_" + uuid.uuid4().hex[:8],
            "name": name,
            "market": market,
            "potential": potential,
            "status": "ACTIVE",
            "created": time.time()
        }

        self.companies.append(company)

        print(
            f"🏢 Company registered: {name}"
        )

        return company


    def analyze_portfolio(self):

        return {
            "system": self.system,
            "companies": len(self.companies),
            "active": len(
                [
                    c for c in self.companies
                    if c["status"] == "ACTIVE"
                ]
            ),
            "timestamp": time.time()
        }


company_portfolio = CompanyPortfolio()
