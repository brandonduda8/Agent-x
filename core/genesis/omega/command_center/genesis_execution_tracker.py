import time


class GenesisExecutionTracker:

    def __init__(self):
        self.system = "GENESIS EXECUTION TRACKER v1"
        self.actions = []

    def record(self, category, action, status="STARTED"):

        entry = {
            "category": category,
            "action": action,
            "status": status,
            "timestamp": time.time()
        }

        self.actions.append(entry)

        return {
            "system": self.system,
            "status": "RECORDED",
            "entry": entry,
            "total_actions": len(self.actions),
            "timestamp": time.time()
        }

    def report(self):

        return {
            "system": self.system,
            "status": "ONLINE",
            "total_actions": len(self.actions),
            "actions": self.actions,
            "timestamp": time.time()
        }


genesis_execution_tracker = GenesisExecutionTracker()
