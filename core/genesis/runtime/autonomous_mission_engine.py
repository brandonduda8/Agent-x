import time


class GenesisAutonomousMissionEngine:


    def __init__(
        self,
        goals,
        planner,
        allocator
    ):

        self.goals = goals
        self.planner = planner
        self.allocator = allocator


        self.system = (
            "GENESIS AUTONOMOUS MISSION PLANNER v2"
        )


    def generate(
        self,
        objective,
        target,
        opportunity,
        agents
    ):


        goal = self.goals.create_goal(

            objective,

            target

        )


        mission = self.planner.create(

            goal,

            opportunity

        )


        assignments = self.allocator.assign(

            mission,

            agents

        )


        return {

            "system":
                self.system,

            "goal":
                goal,

            "mission":
                mission,

            "execution_plan":
                assignments,

            "status":
                "MISSION_READY",

            "timestamp":
                time.time()

        }
