import uuid
import time


class OpportunityScanner:

    def scan(self):

        opportunities = [
            {
                "market":"Dental AI",
                "score":88
            },
            {
                "market":"Legal AI",
                "score":84
            },
            {
                "market":"Real Estate AI",
                "score":86
            }
        ]

        best = max(
            opportunities,
            key=lambda x:x["score"]
        )

        result = {
            "id":f"opportunity_{uuid.uuid4().hex[:8]}",
            "market":best["market"],
            "score":best["score"],
            "decision":"CREATE COMPANY",
            "timestamp":time.time()
        }

        print(
            f"🔎 Opportunity discovered: {best['market']}"
        )

        return result


opportunity_scanner = OpportunityScanner()
