import time


class GenesisCredentialAudit:


    def __init__(self):

        self.system = (
            "GENESIS CREDENTIAL AUDIT v1"
        )

        self.logs = []


    def record(
        self,
        event
    ):

        entry = {

            "event":
                event,

            "timestamp":
                time.time()

        }

        self.logs.append(entry)

        return entry

