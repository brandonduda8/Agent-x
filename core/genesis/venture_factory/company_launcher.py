import time
import uuid


class CompanyLauncher:

    def __init__(self):
        self.system = "GENESIS COMPANY LAUNCHER v1"


    def launch(self, venture):

        company = {
            "id": "company_" + uuid.uuid4().hex[:8],
            "name": venture["name"],
            "departments": [
                "Research",
                "Marketing",
                "Sales",
                "Delivery",
                "Support"
            ],
            "status": "ACTIVE",
            "timestamp": time.time()
        }

        print(
            f"🏢 Company launched: {company['name']}"
        )

        return company


company_launcher = CompanyLauncher()
