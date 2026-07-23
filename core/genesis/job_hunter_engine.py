import time
import uuid

from core.genesis.job_source_connector import (
    job_source_connector
)

from core.genesis.skill_match_engine import (
    skill_match_engine
)

from core.genesis.application_agent import (
    application_agent
)


class GenesisJobHunterEngine:

    """
    GENESIS JOB HUNTER ENGINE v1.1

    Finds matching jobs,
    creates applications,
    prepares candidates.
    """

    def __init__(self):

        self.system = (
            "GENESIS JOB HUNTER ENGINE v1.1"
        )

        self.history = []


    def hunt(
        self,
        candidate_profile
    ):

        print(
            "🔎 Genesis scanning jobs..."
        )


        jobs = (
            job_source_connector
            .search_local_database()
        )


        matches = (
            skill_match_engine
            .analyze_jobs(
                jobs
            )
        )


        applications = []


        for match in matches:


            if (
                match["recommendation"]
                ==
                "APPLY_NOW"
            ):


                job = next(
                    (
                        j
                        for j in jobs
                        if (
                            j["title"]
                            ==
                            match["job"]
                        )
                    ),
                    None
                )


                if job:

                    print(
                        "📨 Creating application:",
                        job["title"]
                    )


                    application = (
                        application_agent
                        .create_application(
                            job,
                            candidate_profile
                        )
                    )


                    applications.append(
                        application
                    )


        result = {

            "id":
                "hunt_"
                +
                uuid.uuid4().hex[:8],

            "jobs_found":
                len(jobs),

            "matches":
                len(matches),

            "applications_created":
                len(applications),

            "applications":
                applications,

            "timestamp":
                time.time()
        }


        self.history.append(
            result
        )


        print(
            "🎯 Job Hunt Complete"
        )


        return result



    def report(self):

        return {

            "system":
                self.system,

            "hunts":
                len(self.history),

            "applications_generated":
                sum(
                    len(
                        x["applications"]
                    )
                    for x in self.history
                ),

            "timestamp":
                time.time()
        }



job_hunter_engine = GenesisJobHunterEngine()
