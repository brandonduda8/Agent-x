import time
import uuid


class GenesisAutonomousExecutionPlanner:

    def __init__(self):

        self.system = "GENESIS AUTONOMOUS EXECUTION PLANNER v1"

        self.plans = []


    def create_task(
        self,
        name,
        agent,
        capability
    ):

        return {

            "id":
                "task_" + uuid.uuid4().hex[:8],

            "name":
                name,

            "agent":
                agent,

            "capability":
                capability,

            "status":
                "READY",

            "created":
                time.time()

        }



    def plan(
        self,
        mission,
        team
    ):

        tasks = []


        for member in team:

            agent = member["agent"]

            skills = member["matched_skills"]


            if "lead_generation" in skills:

                tasks.append(
                    self.create_task(
                        "Research and collect qualified leads",
                        agent,
                        "lead_generation"
                    )
                )


            if "sales" in skills:

                tasks.append(
                    self.create_task(
                        "Create outreach strategy and offer",
                        agent,
                        "sales"
                    )
                )


            if "crm" in skills:

                tasks.append(
                    self.create_task(
                        "Create customer pipeline records",
                        agent,
                        "crm"
                    )
                )


            if "coding" in skills:

                tasks.append(
                    self.create_task(
                        "Build required software components",
                        agent,
                        "coding"
                    )
                )


            if "deployment" in skills:

                tasks.append(
                    self.create_task(
                        "Deploy and validate system",
                        agent,
                        "deployment"
                    )
                )


        plan = {

            "id":
                "execution_"
                +
                uuid.uuid4().hex[:8],

            "mission":
                mission["id"],

            "objective":
                mission["objective"],

            "tasks":
                tasks,

            "status":
                "READY",

            "created":
                time.time()

        }


        self.plans.append(plan)


        print(
            "🚀 Autonomous execution plan created"
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



execution_planner = GenesisAutonomousExecutionPlanner()
