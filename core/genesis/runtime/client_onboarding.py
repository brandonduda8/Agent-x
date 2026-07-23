import time
import uuid


class GenesisClientOnboarding:


    def __init__(self):

        self.system = (
            "GENESIS CLIENT ONBOARDING v1"
        )


    def onboard(
        self,
        client
    ):


        return {

            "id":
                "client_" +
                uuid.uuid4().hex[:8],

            "client":
                client,

            "status":
                "ONBOARDED",

            "timestamp":
                time.time()

        }
