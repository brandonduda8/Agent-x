import time


class GenesisWorkforceTracker:


    def __init__(self):

        self.active = []

        self.system = (
            "GENESIS WORKFORCE TRACKER v1"
        )


    def register(
        self,
        team
    ):

        self.active.append(
            team
        )


        return {

            "teams":
                len(self.active),

            "status":
                "TRACKING",

            "timestamp":
                time.time()

        }


    def status(self):

        return {

            "active_teams":
                len(self.active),

            "timestamp":
                time.time()

        }
