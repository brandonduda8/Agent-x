import time
import uuid


class GenesisMissionTaskPlanner:

    def __init__(self):

        self.system = "GENESIS MISSION TASK PLANNER v1"

        self.plans = []


    def create_plan(
        self,
        mission,
        team
    ):

        tasks = []


        for member in team.get("team", []):

            agent = member["agent"]

            for skill in member.get(
                "matched_skills",
                []
            ):

                tasks.append({

                    "id":
                        "task_" + uuid.uuid4().hex[:8],

                    "name":
                        f"Execute {skill} operation",

                    "agent":
                        agent,

                    "capability":
                        skill,

                    "status":
                        "READY",

                    "created":
                        time.time()

                })


        plan = {

            "id":
                "task_plan_" + uuid.uuid4().hex[:8],

            "mission":
                mission["id"],

            "tasks":
                tasks,

            "status":
                "READY",

            "created":
                time.time()

        }


        self.plans.append(
            plan
        )


        print(
            "📋 Mission execution plan created"
        )


        return plan



    def report(self):

        return {

            "system":
                self.system,

            "plans":
                len(self.plans),

            "timestamp":
                time.time()

        }



mission_task_planner = GenesisMissionTaskPlanner()
