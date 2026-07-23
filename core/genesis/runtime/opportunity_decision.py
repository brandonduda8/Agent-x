import time


class GenesisOpportunityDecision:


    def analyze(
        self,
        opportunity
    ):


        score = 0


        if opportunity.get("value"):

            score += 50


        if opportunity.get("solution"):

            score += 30


        if opportunity.get("status") == "AVAILABLE":

            score += 20


        action = (

            "EXECUTE"

            if score >= 70

            else

            "REVIEW"

        )


        return {

            "opportunity":
                opportunity["business"],

            "score":
                score,

            "decision":
                action,

            "timestamp":
                time.time()

        }
