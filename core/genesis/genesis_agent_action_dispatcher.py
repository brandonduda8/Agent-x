import time
import uuid
import json
import os


class GenesisAgentActionDispatcher:

    def __init__(self):

        self.system = (
            "GENESIS AGENT ACTION DISPATCHER v1"
        )

        self.file = (
            "data/genesis_agent_tasks.json"
        )

        self.tasks = []

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(self.file, "r") as f:
                    data = json.load(f)
                    self.tasks = data.get(
                        "tasks",
                        []
                    )

            except:

                self.tasks = []


    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(self.file, "w") as f:

            json.dump(
                {
                    "system":
                        self.system,

                    "tasks":
                        self.tasks,

                    "updated":
                        time.time()

                },
                f,
                indent=2
            )


    def create_task(
        self,
        mission,
        agent
    ):

        task = {

            "id":
                "task_" +
                uuid.uuid4().hex[:8],

            "mission_id":
                mission.get(
                    "id"
                ),

            "objective":
                mission.get(
                    "objective"
                ),

            "agent":
                agent,

            "instructions":
                self.generate_instruction(
                    agent,
                    mission.get(
                        "objective"
                    )
                ),

            "status":
                "QUEUED",

            "created":
                time.time()

        }


        self.tasks.append(
            task
        )

        self.save()


        print(
            f"📌 Task Created: {agent}"
        )


        return task



    def generate_instruction(
        self,
        agent,
        objective
    ):

        instructions = {

            "Market Research Agent":
                "Research target companies and identify opportunities",

            "Lead Generation Agent":
                "Create qualified prospect lists",

            "Sales Pipeline Agent":
                "Organize prospects into sales stages",

            "Outreach Agent":
                "Generate personalized outreach campaigns",

            "Workflow Automation Agent":
                "Design automation solutions"

        }


        return instructions.get(
            agent,
            "Analyze and complete assigned objective"
        )



    def dispatch_mission(
        self,
        mission
    ):

        created = []


        for agent in mission.get(
            "agents",
            []
        ):

            created.append(
                self.create_task(
                    mission,
                    agent
                )
            )


        return {

            "mission_id":
                mission.get(
                    "id"
                ),

            "tasks_created":
                len(created),

            "tasks":
                created,

            "status":
                "DISPATCHED",

            "timestamp":
                time.time()

        }



    def complete_task(
        self,
        task_id,
        result
    ):

        for task in self.tasks:

            if task["id"] == task_id:

                task["status"] = (
                    "COMPLETE"
                )

                task["result"] = result

                task["completed"] = (
                    time.time()
                )


        self.save()



    def report(self):

        return {

            "system":
                self.system,

            "tasks":
                len(self.tasks),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_agent_action_dispatcher = (
    GenesisAgentActionDispatcher()
)
