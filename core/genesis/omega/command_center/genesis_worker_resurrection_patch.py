from core.genesis.omega.omega_bootstrap import (
    genesis_omega_bootstrap
)

class GenesisWorkerResurrectionPatch:

    def __init__(self):
        self.system = "GENESIS WORKER RESURRECTION BRIDGE PATCH v1"

    def resurrect(self):
        if genesis_omega_bootstrap:

            result = genesis_omega_bootstrap.start()

            return {
                "system": self.system,
                "status": "BOOTSTRAP_RESTORED",
                "bootstrap": result
            }

        return {
            "system": self.system,
            "status": "NO_BOOTSTRAP_AVAILABLE"
        }


genesis_worker_resurrection_patch = GenesisWorkerResurrectionPatch()
