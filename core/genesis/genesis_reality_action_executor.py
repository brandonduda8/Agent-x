import time
import json
import os
import uuid


class GenesisRealityActionExecutor:

    def __init__(self):
        self.file = "data/genesis_reality_actions.json"
        self.actions = []
        self.load()


    def load(self):
        try:
            if os.path.exists(self.file):
                with open(self.file, "r") as f:
                    self.actions = json.load(f)
        except Exception:
            self.actions = []


    def save(self):
        os.makedirs("data", exist_ok=True)

        with open(self.file, "w") as f:
            json.dump(
                self.actions,
                f,
                indent=2
            )


    def create_action(self, category, objective, agent, priority="HIGH"):

        action = {
            "id": "action_" + uuid.uuid4().hex[:8],
            "category": category,
            "objective": objective,
            "agent": agent,
            "priority": priority,
            "status": "CREATED",
            "result": None,
            "created": time.time()
        }

        self.actions.append(action)
        self.save()

        return action


    def update_status(self, action_id, status, result=None):

        for action in self.actions:

            if action["id"] == action_id:
                action["status"] = status
                action["result"] = result
                action["updated"] = time.time()

        self.save()


    def status(self):

        return {
            "system": "GENESIS REALITY ACTION EXECUTOR v1",
            "status": "ONLINE",
            "actions": self.actions,
            "count": len(self.actions),
            "timestamp": time.time()
        }


action_executor = GenesisRealityActionExecutor()
