import uuid
import time


class CapitalDistribution:

    def allocate(self, companies):

        allocations = []

        for company in companies:

            allocations.append({
                "company": company["company"],
                "capital": 5000,
                "priority": "GROWTH"
            })


        result = {
            "id": f"capital_{uuid.uuid4().hex[:8]}",
            "allocations": allocations,
            "timestamp": time.time()
        }

        print(
            "💰 Capital distributed"
        )

        return result


capital_distribution = CapitalDistribution()
