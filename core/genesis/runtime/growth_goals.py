import time
import uuid


class GenesisGrowthGoals:


    def __init__(self):

        self.goals = []


    def create(
        self,
        objective,
        target
    ):

        goal = {

            "id":
                "growth_goal_" +
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
