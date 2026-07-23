import time


class IntegrationRegistry:


    def __init__(self):

        self.connectors = {}


    def register(self, connector):

        self.connectors[
            connector.name
        ] = connector


    def status(self):

        return {

            "system":
            "GENESIS INTEGRATION HUB v1",

            "integrations":
            [
                c.health()
                for c in self.connectors.values()
            ],

            "timestamp":
            time.time()

        }
