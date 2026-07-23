import time


class GenesisLeadScoringEngine:


    def __init__(self):

        self.system = (
            "GENESIS LEAD SCORING ENGINE v1"
        )


    def score(
        self,
        business,
        problems
    ):

        score = 50


        score += len(problems) * 10


        return {

            "business":
                business,

            "score":
                min(score,100),

            "classification":
                "HIGH_VALUE"
                if score >= 80
                else "STANDARD",

            "timestamp":
                time.time()

        }
