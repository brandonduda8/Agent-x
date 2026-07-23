import time
import uuid


class GenesisMissionExecutionEngine:

    def __init__(self):

        self.system = "GENESIS MISSION EXECUTION ENGINE v2"

        self.executions = []



    def select_workers(
        self,
        departments,
        workers
    ):

        selected = []

        for worker in workers:

            capability = worker.get(
                "capability",
                ""
            ).lower()

            for department in departments:

                if department.lower() in capability:

                    selected.append(
                        worker
                    )

                    break


        # fallback: use all available workers

        if not selected:

            selected = workers


        return selected



    def create_tasks(
        self,
        objective,
        departments
    ):

        tasks = []


        for department in departments:

            tasks.append(

                {
                    "department":
                        department,

                    "objective":
                        objective,

                    "task":
                        f"{department} execution for: {objective}",

                    "status":
                        "READY"

                }

            )


        return tasks



    def execute(
        self,
        mission,
        worker_registry
    ):

        print(
            "⚡ Genesis Mission Execution Started"
        )


        workers = worker_registry.get_online_workers()


        departments = mission.get(
            "departments",
            []
        )


        selected_workers = self.select_workers(
            departments,
            workers
        )


        tasks = self.create_tasks(
            mission["objective"],
            departments
        )


        results = []


        for worker in selected_workers:

            print(
                "🤖 Dispatching:",
                worker["name"]
            )


            result = {

                "worker":
                    worker["name"],

                "objective":
                    mission["objective"],

                "status":
                    "COMPLETED",

                "output":
                    "Task completed successfully",

                "timestamp":
                    time.time()

            }


            results.append(
                result
            )


            worker["missions"] += 1



        execution = {

            "id":
                "execution_"
                +
                uuid.uuid4().hex[:8],

            "mission":
                mission["id"],

            "objective":
                mission["objective"],

            "departments":
                departments,

            "tasks":
                tasks,

            "workers":
                [
                    worker["name"]
                    for worker in selected_workers
                ],

            "results":
                results,

            "status":
                "COMPLETE",

            "created":
                time.time()

        }


        self.executions.append(
            execution
        )


        print(
            "🧬 Mission Execution Complete"
        )


        return execution



    def report(self):

        return {

            "system":
                self.system,

            "executions":
                len(
                    self.executions
                ),

            "timestamp":
                time.time()

        }



mission_execution_engine = GenesisMissionExecutionEngine()
