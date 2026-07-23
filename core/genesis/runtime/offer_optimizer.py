import time


class GenesisOfferOptimizer:


    def analyze(
        self,
        offers
    ):

        return {

            "recommended_offer":

                offers[0]
                if offers
                else None,

            "reason":

                "Prioritize highest value offer",

            "timestamp":
                time.time()

        }
