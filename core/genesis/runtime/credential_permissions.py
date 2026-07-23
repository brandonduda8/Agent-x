import time


class GenesisCredentialPermissions:


    def __init__(self):

        self.system = (
            "GENESIS CREDENTIAL PERMISSIONS v1"
        )


    def authorize(
        self,
        connector,
        credential
    ):

        return {

            "connector":
                connector,

            "credential":
                credential,

            "authorized":
                True,

            "timestamp":
                time.time()

        }
