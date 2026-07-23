import time


class GenesisOmegaWorkerAdapter:

    """
    GENESIS OMEGA UNIVERSAL WORKER ADAPTER v1

    Normalizes all worker execution interfaces.

    Supported:
    - execute()
    - run()
    - start()
    - callable workers
    """


    def __init__(
        self,
        worker,
        name=None
    ):

        self.worker = worker

        self.name = (
            name
            or getattr(
                worker,
                "name",
                type(worker).__name__
            )
        )


    def execute(
        self,
        task
    ):

        print(
            "🔌 Worker Adapter:",
            self.name
        )


        try:

            if hasattr(
                self.worker,
                "execute"
            ):

                return self.worker.execute(
                    task
                )


            if hasattr(
                self.worker,
                "run"
            ):

                return self.worker.run(
                    task
                )


            if hasattr(
                self.worker,
                "start"
            ):

                return self.worker.start(
                    task
                )


            if callable(
                self.worker
            ):

                return self.worker(
                    task
                )


            return {

                "status":
                    "NO_EXECUTION_METHOD",

                "worker":
                    self.name,

                "message":
                    "Worker requires execution implementation"

            }


        except Exception as e:


            return {

                "status":
                    "FAILED",

                "worker":
                    self.name,

                "error":
                    str(e)

            }



    def report(self):

        return {

            "worker":
                self.name,

            "adapter":
                "GENESIS OMEGA UNIVERSAL WORKER ADAPTER v1",

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }
