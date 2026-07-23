import time


class GenesisOutreachGenerator:


    def __init__(self):

        self.system = (
            "GENESIS OUTREACH GENERATOR v1"
        )


    def create(
        self,
        analysis,
        offer
    ):


        message = (

            "Hi, we noticed your business may "
            "have opportunities to improve "
            "customer response and follow-up. "
            "We build AI automation systems "
            "that help businesses capture more "
            "leads and save time."

        )


        return {

            "business":
                analysis["business"],

            "message":
                message,

            "offer":
                offer["offer"]["name"],

            "timestamp":
                time.time()

        }
