class GenesisModelScoring:


    def score(
        self,
        model,
        capability
    ):

        score = 0


        if capability in model.get(
            "capabilities",
            []
        ):

            score += 50


        if model.get(
            "tier"
        ) == "FREE":

            score += 20


        if model.get(
            "status"
        ) == "AVAILABLE":

            score += 20


        if model.get(
            "speed",
            0
        ):

            score += model["speed"]


        return score



    def rank(
        self,
        models,
        capability
    ):

        ranked = []


        for model in models:

            ranked.append({

                "model":
                model,

                "score":
                self.score(
                    model,
                    capability
                )

            })


        return sorted(

            ranked,

            key=lambda x:
            x["score"],

            reverse=True

        )
