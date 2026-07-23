import time


class GenesisFollowUpEngine:


    def __init__(self):

        self.system = (
            "GENESIS FOLLOW UP ENGINE v1"
        )


    def create_sequence(
        self,
        business
    ):


        return {

            "business":
                business,

            "sequence":
                [

                "Initial message",

                "Follow-up after 3 days",

                "Follow-up after 7 days",

                "Final check-in"

                ],

            "status":
                "ACTIVE",

            "timestamp":
                time.time()

        }
