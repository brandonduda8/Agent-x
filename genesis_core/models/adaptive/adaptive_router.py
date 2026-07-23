import time


class GenesisAdaptiveRouter:


    def __init__(
        self,
        scorer
    ):

        self.scorer = scorer



    def choose(
        self,
        capability,
        models
    ):


        ranked = self.scorer.rank(

            models,

            capability

        )


        if not ranked:

            return {

                "status":
                "NO_MODEL"

            }


        best = ranked[0]


        return {

            "selected_model":
            best["model"],

            "score":
            best["score"],

            "capability":
            capability,

            "timestamp":
            time.time()

        }
