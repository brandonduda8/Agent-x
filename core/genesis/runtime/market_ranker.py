import time


class GenesisMarketRanker:


    def rank(
        self,
        industry_scores
    ):

        ranking = sorted(

            industry_scores.items(),

            key=lambda x:x[1],

            reverse=True

        )


        return {

            "ranking":[

                {
                    "industry":item[0],
                    "revenue":item[1]
                }

                for item in ranking

            ],

            "timestamp":
                time.time()

        }
