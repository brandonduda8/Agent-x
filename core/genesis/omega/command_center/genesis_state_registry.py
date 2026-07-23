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


try:
    from core.genesis.omega.command_center.heartbeat import (
        genesis_heartbeat_system
    )
except Exception:
    genesis_heartbeat_system = None



class GenesisOmegaStateRegistry:

    """
    GENESIS OMEGA STATE REGISTRY v1

    Single source of truth for Command Center.

    Connects:
    - Workers
    - Missions
    - Approvals
    - Events
    - Decisions
    - Heartbeat
    """


    def __init__(self):

        self.system = (
            "GENESIS OMEGA STATE REGISTRY v1"
        )


        self.worker_fabric = (
            genesis_omega_worker_fabric
        )


        self.missions = (
            genesis_mission_database
        )


        self.approvals = (
            genesis_approval_system
        )


        self.events = (
            genesis_event_bus
        )


        self.decisions = (
            genesis_decision_gate
        )


        self.heartbeat = (
            genesis_heartbeat_system
        )



    def snapshot(self):

        state = {

            "system":
                self.system,


            "workers":
                self.worker_fabric.report(),


            "missions":
                self.missions.report(),


            "approvals":
                self.approvals.report(),


            "timestamp":
                time.time()

        }


        if self.events:

            try:
                state["events"] = (
                    self.events.report()
                )

            except Exception:

                state["events"] = (
                    "AVAILABLE"
                )


        if self.decisions:

            try:
                state["decisions"] = (
                    self.decisions.report()
                )

            except Exception:

                state["decisions"] = (
                    "AVAILABLE"
                )


        if self.heartbeat:

            try:
                state["heartbeat"] = (
                    self.heartbeat.report()
                )

            except Exception:

                state["heartbeat"] = (
                    "AVAILABLE"
                )


        return state



    def health(self):

        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "workers":
                len(
                    self.worker_fabric.workers
                ),

            "missions":
                len(
                    self.missions.missions
                ),

            "pending_approvals":
                len(
                    self.approvals.pending
                ),

            "timestamp":
                time.time()

        }



genesis_state_registry = (
    GenesisOmegaStateRegistry()
)
