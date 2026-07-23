import time
import uuid


class GenesisExecutionEngine:

    def __init__(self):

        self.name = (
            "GENESIS EXECUTION ENGINE v2"
        )

        self.executions = []


    def execute(
        self,
        mission
    ):

        """
        Compatibility layer.

        Allows Genesis autonomous loop
        to call execute()
        while preserving execute_task()
        """

        return self.execute_task(
            mission
        )


    def execute_task(
        self,
        task
    ):

        print(
            "⚡ Executing task:",
            task["objective"]
        )


        from core.genesis.worker_runtime import (
            worker_runtime
        )


        execution = {

            "id":
                "execution_" +
                uuid.uuid4().hex[:8],

            "task":
                task.get(
                    "id",
                    "unknown"
                ),

            "objective":
                task["objective"],

            "agents":
                task.get(
                    "assigned_agents",
                    []
                ),

            "results":
                [],

            "status":
                "RUNNING",

            "started":
                time.time()

        }


        execution["results"] = (
            worker_runtime.run_team(
                task.get(
                    "assigned_agents",
                    []
                ),

                task["objective"]
            )
        )


        execution["status"] = (
            "COMPLETE"
        )


        execution["completed"] = (
            time.time()
        )


        self.executions.append(
            execution
        )


        print(
            "✅ Real Worker Execution Complete"
        )


        return execution



    def report(self):

        return {

            "system":
                self.name,

            "executions":
                len(
                    self.executions
                ),

            "timestamp":
                time.time()

        }



execution_engine = GenesisExecutionEngine()
