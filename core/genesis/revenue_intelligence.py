import time


class GenesisRevenueIntelligence:


    def __init__(self):

        self.name = "GENESIS REVENUE INTELLIGENCE v1"

        self.history = []



    def analyze(self, idea):

        score = {

            "market_demand":
                8,

            "competition":
                7,

            "monetization":
                9,

            "build_difficulty":
                6,

            "customer_access":
                7

        }


        overall = int(

            (

                score["market_demand"]

                +

                score["competition"]

                +

                score["monetization"]

                +

                score["build_difficulty"]

                +

                score["customer_access"]

            )

            / 50

            *

            100

        )


        result = {

            "idea":
                idea,

            "scores":
                score,

            "overall_score":
                overall,

            "recommendation":
                "BUILD"

                if overall >= 70

                else

                "REVIEW",

            "timestamp":
                time.time()

        }


        self.history.append(result)


        return result



    def report(self):

        return {

            "engine":
                self.name,

            "analyzed":
                len(self.history)

        }



revenue_intelligence = GenesisRevenueIntelligence()
