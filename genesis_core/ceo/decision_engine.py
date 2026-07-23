import time


class GenesisDecisionEngine:


    def decide(
        self,
        opportunities
    ):

        ranked = sorted(

            opportunities,

            key=lambda x: x.get(
                "score",
                0
            ),

            reverse=True

        )


        if not ranked:

            return {

                "decision":
                "NO_ACTION",

                "timestamp":
                time.time()

            }


        winner = ranked[0]


        return {

            "decision":
            "EXECUTE",

            "priority_opportunity":
            winner,

            "timestamp":
            time.time()

        }
