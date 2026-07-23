import time

from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)

from core.genesis.omega.command_center.mission_database import (
    genesis_mission_database
)

from core.genesis.omega.command_center.approval_system import (
    genesis_approval_system
)


try:
    from core.genesis.omega.command_center.event_bus import (
        genesis_event_bus
    )
except Exception:
    genesis_event_bus = None


try:
    from core.genesis.omega.command_center.decision_gate import (
        genesis_decision_gate
    )
except Exception:
    genesis_decision_gate = None


class GenesisOmegaStateRegistryCompatibility:

    """
    GENESIS OMEGA STATE REGISTRY COMPATIBILITY v5

    Live system observer.

    Reads current runtime state instead of stale imports.
    """

    def __init__(self):

        self.system = (
            "GENESIS OMEGA STATE REGISTRY COMPATIBILITY v5"
        )

        self.history = []


    def report(self):

        state = {

            "system": self.system,

            "workers":
                genesis_omega_worker_fabric.report(),

            "missions":
                genesis_mission_database.report(),

            "approvals":
                genesis_approval_system.report(),

            "timestamp":
                time.time()
        }


        if genesis_event_bus:

            try:
                state["events"] = (
                    genesis_event_bus.report()
                )
            except Exception:
                state["events"] = {
                    "status": "AVAILABLE"
                }


        if genesis_decision_gate:

            try:
                state["decisions"] = (
                    genesis_decision_gate.report()
                )
            except Exception:
                state["decisions"] = {
                    "status": "AVAILABLE"
                }


        self.history.append(state)


        print(
            "🧠 Genesis State Registry Synced"
        )


        return state



    def health(self):

        return {

            "system": self.system,

            "status": "ONLINE",

            "workers":
                len(
                    genesis_omega_worker_fabric.workers
                ),

            "missions":
                len(
                    genesis_mission_database.missions
                ),

            "pending_approvals":
                len(
                    genesis_approval_system.pending
                ),

            "timestamp":
                time.time()
        }



genesis_state_registry_bridge = (
    GenesisOmegaStateRegistryCompatibility()
)
