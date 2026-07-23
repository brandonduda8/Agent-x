import time


class GenesisPriorityEngine:


    def rank(self, opportunities):

        ranked = sorted(

            opportunities,

            key=lambda x:
            1 if x["priority"] == "HIGH"
            else 0,

            reverse=True

        )


        return {

            "ranked_opportunities":
            ranked,

            "recommended_focus":
            ranked[0]
            if ranked
            else None,

            "timestamp":
            time.time()

        }
