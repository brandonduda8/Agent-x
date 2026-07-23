import time
import uuid


class GenesisGoalManager:


    def __init__(self):

        self.goals = []


    def create_goal(
        self,
        objective,
        target
    ):

        goal = {

            "id":
                "goal_" +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "target":
                target,

            "status":
                "ACTIVE",

            "timestamp":
                time.time()

        }


        self.goals.append(goal)

        return goal


    def all(self):

        return self.goals
