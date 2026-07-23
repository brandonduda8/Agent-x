import time
import uuid


class GenesisJobCreator:


    def create(
        self,
        title,
        skills,
        payment
    ):


        return {

            "id":
                "job_" +
                uuid.uuid4().hex[:8],

            "title":
                title,

            "required_skills":
                skills,

            "payment":
                payment,

            "status":
                "OPEN",

            "timestamp":
                time.time()

        }
