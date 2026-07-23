import time
import uuid


class GenesisMissionTaskGenerator:


    def __init__(self):

        self.system = (
            "GENESIS MISSION TASK GENERATOR v1"
        )



    def generate(
        self,
        mission,
        agent_matches
    ):

        tasks = []


        for capability, agents in agent_matches.items():

            for agent in agents:

                tasks.append({

                    "id":
                        "task_" +
                        uuid.uuid4().hex[:8],

                    "mission":
                        mission,

                    "capability":
                        capability,

                    "agent":
                        agent,

                    "status":
                        "QUEUED"

                })


        return {

            "tasks":
                tasks,

            "created":
                time.time()

        }
