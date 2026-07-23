import time


class GenesisCredentialStore:


    def __init__(self):

        self.system = (
            "GENESIS CREDENTIAL STORE v1"
        )

        self.credentials = {}


    def store(
        self,
        name,
        value
    ):

        self.credentials[name] = {

            "value":
                value,

            "created":
                time.time()

        }

        return {

            "credential":
                name,

            "status":
                "STORED",

            "timestamp":
                time.time()

        }


    def retrieve(
        self,
        name
    ):

        return self.credentials.get(
            name
        )

