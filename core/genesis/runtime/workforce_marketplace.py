import time


class GenesisWorkforceMarketplace:


    def __init__(
        self,
        workers,
        jobs,
        matcher
    ):

        self.workers = workers
        self.jobs = jobs
        self.matcher = matcher


        self.system = (
            "GENESIS GLOBAL WORKFORCE MARKETPLACE v1"
        )


    def create_job(
        self,
        title,
        skills,
        payment
    ):

        return self.jobs.create(

            title,

            skills,

            payment

        )


    def find_workers(
        self,
        job
    ):

        return self.matcher.match(

            job,

            self.workers.all()

        )
