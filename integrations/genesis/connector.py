import time


class GenesisConnector:

    name = "GENESIS CONNECTOR"

    def __init__(self):
        self.status = "INITIALIZED"


    def health(self):

        return {
            "connector": self.name,
            "status": self.status,
            "timestamp": time.time()
        }


    def connect(self):

        self.status = "CONNECTED"

        return self.health()


    def disconnect(self):

        self.status = "DISCONNECTED"

        return self.health()
