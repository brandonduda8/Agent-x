import time
import uuid


class GenesisCompanyState:


    def __init__(self):

        self.companies = []


    def create(
        self,
        name,
        industry
    ):

        company = {

            "id":
                "company_" +
                uuid.uuid4().hex[:8],

            "name":
                name,

            "industry":
                industry,

            "status":
                "ACTIVE",

            "clients":
                0,

            "revenue":
                0,

            "timestamp":
                time.time()

        }


        self.companies.append(company)

        return company


    def update_revenue(
        self,
        company_id,
        amount
    ):

        for company in self.companies:

            if company["id"] == company_id:

                company["revenue"] += amount

                return company


        return None
