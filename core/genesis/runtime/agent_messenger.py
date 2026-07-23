import time
import uuid


class GenesisAgentMessenger:


    def __init__(self):

        self.system = (
            "GENESIS AGENT MESSENGER v1"
        )


    def send(
        self,
        sender,
        receiver,
        message
    ):

        return {

            "id":
                "message_" +
                uuid.uuid4().hex[:8],

            "from":
                sender,

            "to":
                receiver,

            "message":
                message,

            "timestamp":
                time.time()

        }
