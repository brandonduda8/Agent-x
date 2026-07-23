import time


class GenesisRevenueScoringEngine:


    def score(
        self,
        opportunity
    ):


        score = 0


        if opportunity.get(
            "problem"
        ):

            score += 25


        if opportunity.get(
            "business_value"
        ):

            score += 25


        if opportunity.get(
            "recurring"
        ):

            score += 25


        if opportunity.get(
            "easy_delivery"
        ):

            score += 25



        return {

            "opportunity":
                opportunity.get("name"),

            "revenue_score":
                score,

            "timestamp":
                time.time()

        }
