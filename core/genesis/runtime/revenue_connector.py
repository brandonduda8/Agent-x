import time


class GenesisRevenueConnector:


    def __init__(self):

        self.name = (
            "Revenue Connector"
        )


    def create_lead(
        self,
        business
    ):

        return {

            "connector":
                self.name,

            "lead":
                business,

            "status":
                "CREATED",

            "timestamp":
                time.time()

        }
