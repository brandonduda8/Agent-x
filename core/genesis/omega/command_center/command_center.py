import time

from core.genesis.omega.command_center.event_bus import (
    genesis_event_bus
)

from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)


class GenesisOmegaCommandCenter:

    """
    GENESIS OMEGA COMMAND CENTER v1

    Human control layer.
    """

    def __init__(self):

        self.system = (
            "GENESIS OMEGA COMMAND CENTER v1"
        )



    def dashboard(self):

        return {

            "system":
                self.system,


            "workers":
                genesis_omega_worker_fabric.report(),


            "events":
                genesis_event_bus.recent(),


            "status":
                "ONLINE",


            "timestamp":
                time.time()
        }



    def broadcast(
        self,
        message
    ):

        return genesis_event_bus.emit(
            "COMMAND",
            "HUMAN_OPERATOR",
            message
        )



    def agent_report(
        self,
        worker,
        message,
        data=None
    ):

        return genesis_event_bus.emit(
            "AGENT_REPORT",
            worker,
            message,
            data
        )



genesis_command_center = GenesisOmegaCommandCenter()
