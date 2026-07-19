import uuid
import time


class CompanyRanker:

    def rank(self, companies):

        ranked = []

        for company in companies:

            ranked.append({
                "company": company["company"],
                "score": 90,
                "priority": "HIGH"
            })


        result = {
            "id": f"ranking_{uuid.uuid4().hex[:8]}",
            "companies": ranked,
            "timestamp": time.time()
        }

        print(
            "📊 Companies ranked"
        )

        return result


company_ranker = CompanyRanker()
