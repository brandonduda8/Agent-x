import time


class GenesisWorkerMatching:


    def match(
        self,
        job,
        workers
    ):


        matches = []


        for worker in workers:


            if any(

                skill in worker["skills"]

                for skill in job["skills"]

            ):

                matches.append(worker)


        return {

            "job":
                job["id"],

            "matches":
                matches,

            "timestamp":
                time.time()

        }
