import time


class GenesisVentureScoring:


    def score(
        self,
        venture
    ):


        score = 0


        if venture.get("industry"):

            score += 50


        if venture.get("revenue",0) > 0:

            score += 30


        if venture.get("status") == "ACTIVE":

            score += 20


        return {

            "venture":
                venture["name"],

            "score":
                score,

            "timestamp":
                time.time()

        }
