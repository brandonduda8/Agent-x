import time

from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)

try:
    from core.genesis.omega.bootstrap import (
        genesis_omega_bootstrap
    )
except Exception:
    genesis_omega_bootstrap = None


class GenesisWorkerResurrection:
    """
    GENESIS WORKER RESURRECTION BRIDGE v1

    Ensures worker fabric is populated.
    """

    def __init__(self):
        self.system = (
            "GENESIS WORKER RESURRECTION BRIDGE v1"
        )
        self.attempts = 0


    def revive(self):

        self.attempts += 1

        current = (
            genesis_omega_worker_fabric.report()
        )

        if current.get("workers", 0) > 0:
            return {
                "system": self.system,
                "status": "HEALTHY",
                "workers": current,
                "timestamp": time.time()
            }


        if genesis_omega_bootstrap:

            try:
                result = (
                    genesis_omega_bootstrap.start()
                )

                return {
                    "system": self.system,
                    "status": "BOOTSTRAP_RESTORED",
                    "result": result,
                    "timestamp": time.time()
                }

            except Exception as e:

                return {
                    "system": self.system,
                    "status": "FAILED",
                    "error": str(e),
                    "timestamp": time.time()
                }


        return {
            "system": self.system,
            "status": "NO_BOOTSTRAP_FOUND",
            "timestamp": time.time()
        }


genesis_worker_resurrection = (
    GenesisWorkerResurrection()
)
