import os
import json
import time
import uuid


class GenesisEmergencyCommandEngine:

    def __init__(self):

        self.system = (
            "GENESIS EMERGENCY COMMAND ENGINE v1"
        )

        self.file = (
            "data/genesis_emergency_status.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    self.state = json.load(f)

            except:

                self.state = self.default_state()

        else:

            self.state = self.default_state()
            self.save()


    def default_state(self):

        return {

            "system":
                self.system,

            "mission":
                "Stabilize life while building Genesis revenue",

            "priority_levels": {

                "critical": [

                    "Generate immediate income",
                    "Maintain communication access",
                    "Protect housing stability"

                ],

                "high": [

                    "Close first AI automation client",
                    "Build daily revenue pipeline"

                ],

                "growth": [

                    "Expand Genesis agents",
                    "Build automation systems"

                ]

            },

            "completed_tasks": [],

            "active_tasks": [],

            "created":
                time.time()

        }


    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.state,
                f,
                indent=2
            )


    def create_daily_plan(self):

        plan = {

            "id":
                "daily_" + uuid.uuid4().hex[:8],

            "date":
                time.time(),

            "tasks": [

                {
                    "priority":
                        "CRITICAL",

                    "task":
                        "Complete revenue producing action"
                },

                {
                    "priority":
                        "HIGH",

                    "task":
                        "Contact qualified prospects"
                },

                {
                    "priority":
                        "GROWTH",

                    "task":
                        "Improve Genesis system"
                }

            ]

        }


        self.state["active_tasks"] = plan["tasks"]

        self.save()

        return plan


    def complete_task(
        self,
        task
    ):

        self.state[
            "completed_tasks"
        ].append(
            {
                "task": task,
                "completed": time.time()
            }
        )

        self.save()


    def status(self):

        return {

            "system":
                self.system,

            "active_tasks":
                len(
                    self.state["active_tasks"]
                ),

            "completed_tasks":
                len(
                    self.state["completed_tasks"]
                ),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_emergency_command_engine = (
    GenesisEmergencyCommandEngine()
)
