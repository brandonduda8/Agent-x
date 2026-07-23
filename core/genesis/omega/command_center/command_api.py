import time

from core.genesis.omega.command_center.genesis_state_registry import (
    genesis_state_registry
)

from core.genesis.omega.command_center.mission_database import (
    genesis_mission_database
)

from core.genesis.omega.command_center.approval_system import (
    genesis_approval_system
)

from core.genesis.omega.command_center.decision_gate import (
    genesis_decision_gate
)


class GenesisOmegaCommandAPI:
    """
    GENESIS OMEGA COMMAND API v1

    External control interface.

    Provides:
    - system status
    - mission creation
    - approvals
    - decisions
    - state access
    """

    def __init__(self):

        self.system = (
            "GENESIS OMEGA COMMAND API v1"
        )


    def status(self):

        return {
            "system": self.system,
            "status": "ONLINE",
            "timestamp": time.time()
        }


    def state(self):

        return genesis_state_registry.snapshot()


    def missions(self):

        return (
            genesis_mission_database.list_all()
        )


    def create_mission(
        self,
        objective
    ):

        return (
            genesis_mission_database.create(
                objective
            )
        )


    def approvals(self):

        return {
            "pending":
                genesis_approval_system.pending,

            "history":
                genesis_approval_system.history
        }


    def approve(
        self,
        approval_id
    ):

        return (
            genesis_approval_system.approve(
                approval_id
            )
        )


    def reject(
        self,
        approval_id
    ):

        return (
            genesis_approval_system.reject(
                approval_id
            )
        )


    def decisions(self):

        return (
            genesis_decision_gate.report()
        )


    def report(self):

        return {
            "system":
                self.system,

            "status":
                "ONLINE",

            "capabilities":
                [
                    "state",
                    "missions",
                    "approvals",
                    "decisions",
                    "commands"
                ],

            "timestamp":
                time.time()
        }



genesis_command_api = GenesisOmegaCommandAPI()
