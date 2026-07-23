import time


class GenesisOpportunityRanker:


    def rank(
        self,
        opportunities
    ):


        ranked = sorted(

            opportunities,

            key=lambda x:
                x["score"],

            reverse=True

        )


        return {

            "ranked_opportunities":
                ranked,

            "timestamp":
                time.time()

        }
