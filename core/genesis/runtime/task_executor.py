import time


class GenesisTaskExecutor:


    def execute(
        self,
        task,
        worker
    ):


        return {

            "task":
                task,

            "worker":
                worker,

            "status":
                "COMPLETE",

            "result":
                "Task executed",

            "timestamp":
                time.time()

        }
