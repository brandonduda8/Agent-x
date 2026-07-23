import time


class GenesisOpportunityScoring:


    def score(
        self,
        opportunity
    ):

        score = 50


        if "automation" in opportunity["solution"].lower():

            score += 30


        if "lead" in opportunity["problem"].lower():

            score += 20



        return {

            "opportunity":
                opportunity["id"],

            "revenue_score":
                score,

            "priority":

                (
                    "HIGH"
                    if score >= 80
                    else "MEDIUM"
                ),

            "timestamp":
                time.time()

        }
