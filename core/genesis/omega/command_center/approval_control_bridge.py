import time
import uuid

from core.genesis.omega.command_center.approval_system import (
    genesis_approval_system
)


class GenesisOmegaApprovalControlBridge:

    """
    GENESIS OMEGA APPROVAL CONTROL BRIDGE v1

    Exposes human approval state to Command Center.
    """

    def __init__(
        self,
        approval_system=None
    ):

        self.system = (
            "GENESIS OMEGA APPROVAL CONTROL BRIDGE v1"
        )

        self.approval_system = (
            approval_system
            or genesis_approval_system
        )

        self.snapshots = []


    def sync(self):

        pending = (
            self.approval_system.pending
        )

        history = (
            self.approval_system.history
        )

        snapshot = {

            "id":
                "approval_view_"
                + uuid.uuid4().hex[:8],

            "pending":
                pending,

            "history":
                history,

            "pending_count":
                len(pending),

            "history_count":
                len(history),

            "timestamp":
                time.time()

        }


        self.snapshots.append(
            snapshot
        )


        print(
            "🔐 Approval Control Sync:",
            len(pending),
            "pending approvals"
        )


        return snapshot


    def report(self):

        latest = self.sync()

        return {

            "system":
                self.system,

            "pending":
                latest["pending"],

            "history":
                latest["history"],

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }


genesis_approval_control_bridge = (
    GenesisOmegaApprovalControlBridge()
)
