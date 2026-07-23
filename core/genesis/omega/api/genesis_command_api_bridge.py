import time

from core.genesis.omega.api.genesis_command_api import (
    GenesisOmegaCommandAPI
)


class GenesisOmegaCommandAPIBridge:

    """
    GENESIS OMEGA COMMAND API BRIDGE v1

    Connects the dashboard API to
    live Genesis systems.
    """

    def __init__(
        self,
        command_center=None,
        approval_system=None,
        worker_observer=None,
        mission_database=None
    ):

        self.system = (
            "GENESIS OMEGA COMMAND API BRIDGE v1"
        )


        self.api = GenesisOmegaCommandAPI(
            command_center=command_center,
            approval_system=approval_system,
            worker_observer=worker_observer,
            mission_database=mission_database
        )


    def report(self):

        return {

            "system":
                self.system,

            "api":
                self.api.status(),

            "connected":
                {

                "workers":
                    self.api.worker_observer is not None,

                "approvals":
                    self.api.approval_system is not None,

                "missions":
                    self.api.mission_database is not None,

                "command":
                    self.api.command_center is not None

                },

            "timestamp":
                time.time()
        }



genesis_command_api_bridge = (
    GenesisOmegaCommandAPIBridge()
)
