import uuid
import time


class GenesisJobMarketplace:


    def __init__(self):

        self.jobs = {}


    def create_job(
        self,
        title,
        skills,
        payment
    ):

        job_id = (
            "job_" +
            uuid.uuid4().hex[:8]
        )

        self.jobs[job_id] = {

            "id":
                job_id,

            "title":
                title,

            "skills":
                skills,

            "payment":
                payment,

            "status":
                "OPEN",

            "timestamp":
                time.time()

        }


        return self.jobs[job_id]
