import uuid
import time


class CompanyBuilder:

    def build(self, business):

        company = {
            "id":f"company_{uuid.uuid4().hex[:8]}",
            "name":business["name"],
            "market":business["market"],
            "departments":[
                "Research",
                "Marketing",
                "Sales",
                "Delivery",
                "Support"
            ],
            "status":"ACTIVE",
            "timestamp":time.time()
        }

        print(
            f"🏢 Company created: {company['name']}"
        )

        return company


company_builder = CompanyBuilder()
