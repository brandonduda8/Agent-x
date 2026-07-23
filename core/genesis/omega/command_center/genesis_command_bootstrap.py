import time

from core.genesis.omega.omega_bootstrap import (
    genesis_omega_bootstrap
)

from core.genesis.omega.command_center.worker_observer import (
    genesis_worker_observer
)

from core.genesis.omega.command_center.orchestrator import (
    genesis_command_orchestrator
)


class GenesisCommandBootstrap:

    """
    GENESIS OMEGA COMMAND CENTER BOOTSTRAP v1
    """

    def __init__(self):

        self.system = (
            "GENESIS OMEGA COMMAND CENTER BOOTSTRAP v1"
        )


    def start(self):

        print(
            "🚀 Starting Genesis Command Center..."
        )


        omega = (
            genesis_omega_bootstrap.start()
        )


        workers = (
            genesis_worker_observer.sync()
        )


        dashboard = (
            genesis_command_orchestrator.dashboard()
        )


        return {

            "system":
                self.system,

            "omega":
                omega,

            "workers":
                workers,

            "dashboard":
                dashboard,

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_command_bootstrap = GenesisCommandBootstrap()
