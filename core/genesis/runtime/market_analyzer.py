import time


class GenesisMarketAnalyzer:


    def analyze(
        self,
        opportunities
    ):

        rankings = []


        for item in opportunities:

            score = item.get(
                "revenue_score",
                0
            )


            rankings.append({

                "opportunity":
                    item.get(
                        "name",
                        "Unknown"
                    ),

                "score":
                    score

            })


        rankings.sort(

            key=lambda x: x["score"],

            reverse=True

        )


        return {

            "top_markets":
                rankings,

            "timestamp":
                time.time()

        }
