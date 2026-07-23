import time
import uuid


class GenesisAutonomousMissionExecutionPlanner:


    def __init__(
        self,
        matcher,
        task_generator
    ):

        self.matcher = matcher

        self.task_generator = task_generator

        self.system = (
            "GENESIS AUTONOMOUS MISSION EXECUTION PLANNER v1"
        )



    def plan(
        self,
        mission,
        capabilities
    ):

        agent_plan = (
            self.matcher.match(
                capabilities
            )
        )


        task_plan = (
            self.task_generator.generate(
                mission,
                agent_plan["matches"]
            )
        )


        return {

            "id":
                "mission_plan_" +
                uuid.uuid4().hex[:8],

            "system":
                self.system,

            "objective":
                mission,

            "agents":
                agent_plan["matches"],

            "tasks":
                task_plan["tasks"],

            "status":
                "READY_FOR_EXECUTION",

            "timestamp":
                time.time()

        }
