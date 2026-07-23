import time


class GenesisMissionOrchestrator:


    def __init__(
        self,
        decomposer,
        planner,
        selector
    ):

        self.decomposer = decomposer
        self.planner = planner
        self.selector = selector


    def create_mission(
        self,
        objective
    ):

        tasks = self.decomposer.decompose(
            objective
        )


        assignments = []


        for task in tasks:

            assignments.append({

                "task":
                task,

                "agent":
                self.selector.select(
                    task["capability"]
                )

            })


        mission = self.planner.create(
            objective,
            assignments
        )


        return {

            "system":
            "GENESIS AUTONOMOUS MISSION ORCHESTRATOR v1",

            "mission":
            mission,

            "status":
            "READY_FOR_EXECUTION",

            "timestamp":
            time.time()

        }
