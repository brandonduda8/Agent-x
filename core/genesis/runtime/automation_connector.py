import time


class GenesisAutomationConnector:


    def __init__(self):

        self.name = (
            "Automation Connector"
        )


    def create_workflow(
        self,
        objective
    ):

        return {

            "connector":
                self.name,

            "workflow":
                objective,

            "status":
                "CREATED",

            "timestamp":
                time.time()

        }
