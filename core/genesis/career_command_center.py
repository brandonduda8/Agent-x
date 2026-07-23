import time
import uuid

from core.genesis.job_hunter_engine import job_hunter_engine
from core.genesis.mission_learning_engine import mission_learning_engine


class GenesisCareerCommandCenter:
    """
    GENESIS CAREER COMMAND CENTER v1.2

    Controls:
    - job discovery
    - skill matching
    - applications
    - career intelligence learning
    """

    def __init__(self):
        self.system = "GENESIS CAREER COMMAND CENTER v1.2"
        self.missions = []
        self.application_history = []


    def run_mission(self, profile):

        print("🧬 Genesis Career Mission Started")

        mission_id = "career_" + uuid.uuid4().hex[:8]

        mission = {
            "id": mission_id,
            "objective": "Find and apply for suitable remote jobs",
            "profile": profile,
            "status": "ACTIVE",
            "created": time.time()
        }

        result = job_hunter_engine.hunt(profile)

        applications = result.get(
            "applications",
            []
        )

        agents = [
            "Job Hunter Agent",
            "Application Agent"
        ]

        capabilities = [
            "job_matching",
            "application_generation",
            "career_research"
        ]

        print("🧠 Genesis learning from career mission")

        learning_outcome = {

            "mission": mission_id,

            "objective":
                mission["objective"],

            "success_score":
                100 if applications else 50,

            "agents":
                agents,

            "capabilities":
                capabilities,

            "agent_results": [

                {
                    "agent": "Job Hunter Agent",

                    "results": [

                        {
                            "skill":
                                "job_matching",

                            "result":
                                {
                                    "matches":
                                        result.get(
                                            "matches",
                                            0
                                        )
                                }
                        }

                    ]

                },

                {
                    "agent": "Application Agent",

                    "results": [

                        {
                            "skill":
                                "application_generation",

                            "result":
                                {
                                    "applications":
                                        len(applications)
                                }
                        }

                    ]

                }

            ]

        }


        learning = mission_learning_engine.learn(
            learning_outcome
        )


        execution = {

            "id":
                mission_id,

            "jobs_found":
                result.get(
                    "jobs_found",
                    0
                ),

            "matches":
                result.get(
                    "matches",
                    0
                ),

            "applications_created":
                len(applications),

            "applications":
                applications,

            "learning":
                learning,

            "timestamp":
                time.time()

        }


        self.missions.append(
            execution
        )

        self.application_history.extend(
            applications
        )


        print(
            "🎯 Career Mission Complete"
        )

        return execution



    def report(self):

        return {

            "system":
                self.system,

            "missions":
                len(self.missions),

            "applications_created":
                len(
                    self.application_history
                ),

            "timestamp":
                time.time()

        }



career_command_center = GenesisCareerCommandCenter()
