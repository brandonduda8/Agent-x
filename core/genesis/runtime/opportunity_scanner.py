import time
import uuid


class GenesisOpportunityScanner:


    def scan(
        self,
        opportunities
    ):

        results = []


        for item in opportunities:

            results.append({

                "id":
                    "opportunity_" +
                    uuid.uuid4().hex[:8],

                "industry":
                    item["industry"],

                "problem":
                    item["problem"],

                "solution":
                    item["solution"],

                "score":
                    item["value_score"]

            })


        return {

            "opportunities":
                results,

            "timestamp":
                time.time()

        }
