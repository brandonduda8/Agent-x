import time


class GenesisBusinessModelGenerator:


    def create(
        self,
        opportunity
    ):

        return {

            "business_name":
                "AI " +
                opportunity["industry"] +
                " Automation System",

            "customer":
                opportunity["industry"] +
                " businesses",

            "problem":
                opportunity["problem"],

            "solution":
                opportunity["solution"],

            "timestamp":
                time.time()

        }
