import time

from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)

from core.genesis.omega.command_center.genesis_command_dashboard import (
    genesis_command_dashboard
)


class GenesisDashboardGuardian:
    """
    GENESIS DASHBOARD GUARDIAN v1

    Keeps the command center synchronized.
    """

    def __init__(self):
        self.system = (
            "GENESIS DASHBOARD GUARDIAN v1"
        )
        self.repairs = 0


    def stabilize(self):

        workers = (
            genesis_omega_worker_fabric.report()
        )

        if workers.get("workers", 0) == 0:

            try:
                genesis_omega_worker_fabric.sync()
                self.repairs += 1

            except Exception:
                pass


        return {
            "system": self.system,

            "status": "ONLINE",

            "repairs": self.repairs,

            "dashboard": (
                genesis_command_dashboard.snapshot()
            ),

            "timestamp": time.time()
        }



genesis_dashboard_guardian = (
    GenesisDashboardGuardian()
)
