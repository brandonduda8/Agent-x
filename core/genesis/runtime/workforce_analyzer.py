import time


class GenesisWorkforceAnalyzer:


    def analyze(
        self,
        workers
    ):

        ranked = sorted(

            workers,

            key=lambda x:
                x.get(
                    "completed_jobs",
                    0
                ),

            reverse=True

        )


        return {

            "top_workers":
                ranked,

            "timestamp":
                time.time()

        }
