import time


class GenesisExecutionEngine:


    def __init__(
        self,
        queue,
        registry,
        tracker
    ):

        self.queue = queue
        self.registry = registry
        self.tracker = tracker

        self.system = (
            "GENESIS EXECUTION ENGINE v3"
        )


    def execute_task(
        self,
        capability,
        task
    ):

        executors = self.registry.find(
            capability
        )


        if not executors:

            return {

                "status":
                    "NO_EXECUTOR",

                "capability":
                    capability

            }


        executor = executors[0]


        queued = self.queue.add_task(
            task,
            executor
        )


        result = {

            "executor":
                executor,

            "task":
                task,

            "output":
                "Task completed"

        }


        return self.tracker.update(

            queued["id"],

            "COMPLETE",

            result

        )
