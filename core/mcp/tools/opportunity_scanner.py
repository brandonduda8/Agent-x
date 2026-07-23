import time
import uuid


class OpportunityScanner:

    """
    GENESIS OPPORTUNITY SCANNER MCP v1
    """

    def __init__(self):

        self.system = "GENESIS OPPORTUNITY SCANNER MCP v1"

        self.scans = []


    def scan(
        self,
        opportunities
    ):

        ranked = []


        for item in opportunities:

            value = item.get(
                "value",
                0
            )

            skills = item.get(
                "skills",
                []
            )


            score = min(
                value / 100,
                50
            ) + len(skills) * 10


            ranked.append(
                {
                    "id":
                    "opp_" +
                    uuid.uuid4().hex[:8],

                    "title":
                    item.get(
                        "title"
                    ),

                    "value":
                    value,

                    "skills":
                    skills,

                    "score":
                    score,

                    "action":
                    "EXECUTE"
                    if score >= 70
                    else "REVIEW",

                    "timestamp":
                    time.time()
                }
            )


        ranked.sort(
            key=lambda x:x["score"],
            reverse=True
        )


        result = {

            "system":
            self.system,

            "opportunities":
            ranked,

            "timestamp":
            time.time()

        }


        self.scans.append(
            result
        )


        return result



opportunity_scanner = OpportunityScanner()
