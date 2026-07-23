import os
import json
import time
import uuid


class GenesisJobSourceConnector:

    """
    GENESIS JOB SOURCE CONNECTOR v2

    Persistent job intelligence database.

    Stores:
    - remote jobs
    - skills
    - sources
    - pay ranges
    """


    def __init__(self):

        self.system = (
            "GENESIS JOB SOURCE CONNECTOR v2"
        )

        self.file = (
            "data/genesis_jobs.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.initialize()



    def initialize(self):

        if not os.path.exists(
            self.file
        ):

            with open(
                self.file,
                "w"
            ) as f:

                json.dump(
                    {
                        "jobs": []
                    },
                    f,
                    indent=2
                )



    def load(self):

        with open(
            self.file,
            "r"
        ) as f:

            return json.load(f)



    def save(
        self,
        data
    ):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )



    def add_job(
        self,
        title,
        company,
        source,
        job_type,
        skills,
        pay_range,
        url=None
    ):


        data = self.load()


        job = {

            "id":
                "job_"
                +
                uuid.uuid4().hex[:8],


            "title":
                title,


            "company":
                company,


            "source":
                source,


            "type":
                job_type,


            "skills":
                skills,


            "pay_range":
                pay_range,


            "url":
                url,


            "status":
                "NEW",


            "created":
                time.time()

        }


        data["jobs"].append(
            job
        )


        self.save(
            data
        )


        print(
            f"💼 Job Added: {title}"
        )


        return job



    def search_local_database(
        self,
        keyword=None
    ):

        data = self.load()


        jobs = data["jobs"]


        if keyword:

            keyword = keyword.lower()


            jobs = [

                job

                for job in jobs

                if (

                    keyword in job["title"].lower()

                    or

                    any(
                        keyword in skill.lower()

                        for skill in job["skills"]

                    )

                )

            ]


        return jobs



    def analyze_market(self):

        jobs = self.search_local_database()


        print(
            "🧠 Job market analysis complete"
        )


        return {

            "system":
                self.system,


            "available_jobs":
                len(jobs),


            "jobs":
                jobs,


            "timestamp":
                time.time()

        }




job_source_connector = GenesisJobSourceConnector()
