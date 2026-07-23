import time


class GenesisResourceDecision:


    def assign(
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
                job["title"],

            "assigned_workers":
                matches,

            "decision":

                "ASSIGN"

                if matches

                else

                "SEARCH",

            "timestamp":
                time.time()

        }
