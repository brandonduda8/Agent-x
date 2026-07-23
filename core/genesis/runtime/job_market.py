import time
import uuid


class GenesisJobMarket:


    def __init__(self):

        self.jobs = []


    def create(
        self,
        title,
        skills,
        reward
    ):

        job = {

            "id":
                "job_" +
                uuid.uuid4().hex[:8],

            "title":
                title,

            "skills":
                skills,

            "reward":
                reward,

            "status":
                "OPEN",

            "timestamp":
                time.time()

        }


        self.jobs.append(job)

        return job
