import time
import uuid


class GenesisGoalManager:

    def __init__(self):
        self.system = "GENESIS GOAL MANAGER v1"
        self.goals = []


    def create_goal(self, objective):

        goal = {
            "id": "goal_" + uuid.uuid4().hex[:8],
            "objective": objective,
            "status": "ACTIVE",
            "created": time.time()
        }

        self.goals.append(goal)

        print(
            "🎯 Goal registered:",
            objective
        )

        return goal


    def report(self):

        return {
            "system": self.system,
            "goals": len(self.goals),
            "timestamp": time.time()
        }


goal_manager = GenesisGoalManager()
