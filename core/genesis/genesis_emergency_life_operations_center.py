import os
import json
import time
import uuid


class GenesisEmergencyLifeOperationsCenter:

    def __init__(self):

        self.system = (
            "GENESIS EMERGENCY LIFE OPERATIONS CENTER v1"
        )

        self.file = (
            "data/genesis_emergency_command.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
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


    def create_daily_plan(
        self,
        objective="Stabilize life while building income"
    ):

        plan = {

            "id":
                "daily_" + uuid.uuid4().hex[:8],

            "objective":
                objective,

            "tasks":[

                {
                    "priority":
                        "CRITICAL",

                    "category":
                        "income",

                    "task":
                        "Complete one revenue producing action"
                },

                {
                    "priority":
                        "HIGH",

                    "category":
                        "stability",

                    "task":
                        "Complete the most urgent personal stability task"
                },

                {
                    "priority":
                        "GROWTH",

                    "category":
                        "development",

                    "task":
                        "Improve Genesis or personal skills"
                }

            ],

            "created":
                time.time()
        }


        self.tasks.append(plan)

        self.save()

        print(
            "🛟 Genesis Emergency Life Plan Created"
        )

        return plan



    def report(self):

        return {

            "system":
                self.system,

            "active_plans":
                len(self.tasks),

            "status":
                "ONLINE",

            "persistent_memory":
                self.file,

            "timestamp":
                time.time()

        }



genesis_emergency_life_operations_center = (
    GenesisEmergencyLifeOperationsCenter()
)
