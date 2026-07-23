import time


class GenesisActionDispatcher:

    def __init__(self):
        self.system = "GENESIS ACTION DISPATCHER v1"
        self.executions = 0

    def dispatch(self, ranked_missions):

        self.executions += 1

        if not ranked_missions:
            return {
                "system": self.system,
                "status": "NO_ACTIONS",
                "timestamp": time.time()
            }

        target = ranked_missions[0]

        return {
            "system": self.system,
            "status": "ACTION_READY",
            "execution": self.executions,
            "selected_agent": target["agent"],
            "mission": target["mission"],
            "priority_score": target["priority_score"],
            "next_steps": [
                "Research opportunities",
                "Create action list",
                "Begin outreach",
                "Track results"
            ],
            "timestamp": time.time()
        }


genesis_action_dispatcher = GenesisActionDispatcher()
