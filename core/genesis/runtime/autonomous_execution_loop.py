import time


class GenesisAutonomousExecutionLoop:


    def __init__(
        self,
        planner,
        workforce,
        memory
    ):

        self.system = (
            "GENESIS AUTONOMOUS EXECUTION LOOP v1"
        )

        self.planner = planner

        self.workforce = workforce

        self.memory = memory



    def execute(
        self,
        objective
    ):

        print(
            "🚀 Genesis Autonomous Execution Started"
        )


        plan = self.planner.plan(
            objective
        )


        team = self.workforce.build_team(

            [
                task["capability"]
                for task in plan["tasks"]
            ]

        )


        results = []


        for agent in team["agents"]:

            results.append(

                {

                    "agent":
                        agent,

                    "status":
                        "ASSIGNED",

                    "timestamp":
                        time.time()

                }

            )


        memory = self.memory.store(
            plan,
            results
        )


        return {

            "system":
                self.system,

            "mission":
                plan,

            "team":
                team,

            "results":
                results,

            "learning":
                memory,

            "status":
                "COMPLETE"

        }
