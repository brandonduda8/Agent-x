import time

from core.genesis.omega.command_center.state_registry import (
    genesis_state_registry_bridge
)

try:
    from core.genesis.omega.command_center.cycle_bridge import (
        genesis_cycle_bridge
    )
except Exception:
    genesis_cycle_bridge = None


class GenesisCommandDashboard:
    """
    GENESIS NORTH STAR COMMAND DASHBOARD v1

    Unified operational view:
    - system health
    - workers
    - missions
    - autonomous cycles
    - decisions
    """

    def __init__(self):
        self.system = (
            "GENESIS NORTH STAR COMMAND DASHBOARD v1"
        )
        self.views = 0

    def snapshot(self):

        self.views += 1

        state = (
            genesis_state_registry_bridge.report()
        )

        dashboard = {
            "system": self.system,

            "health": {
                "status": "ONLINE"
            },

            "live_state": state,

            "workers": (
                state.get(
                    "workers",
                    {}
                )
            ),

            "missions": (
                state.get(
                    "missions",
                    {}
                )
            ),

            "events": (
                state.get(
                    "events",
                    {}
                )
            ),

            "decisions": (
                state.get(
                    "decisions",
                    {}
                )
            ),

            "autonomous_cycle": {
                "status": "READY"
            },

            "views": self.views,

            "timestamp": time.time()
        }

        return dashboard


    def execute_cycle(self):

        if not genesis_cycle_bridge:
            return {
                "status": "UNAVAILABLE",
                "reason": "cycle bridge missing"
            }

        return genesis_cycle_bridge.start()



genesis_command_dashboard = (
    GenesisCommandDashboard()
)
