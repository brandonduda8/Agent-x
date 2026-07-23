import time
import uuid
import json
import os


class GenesisMissionExecutionEngine:

    def __init__(self):

        self.system = (
            "GENESIS MISSION EXECUTION ENGINE v1"
        )

        self.file = (
            "data/genesis_active_missions.json"
        )

        self.missions = []

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(self.file, "r") as f:
                    data = json.load(f)
                    self.missions = data.get(
                        "missions",
                        []
                    )

            except:

                self.missions = []


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

                    "missions":
                        self.missions,

                    "updated":
                        time.time()

                },
                f,
                indent=2
            )


    def start_mission(
        self,
        execution_plan
    ):

        mission = {

            "id":
                "mission_" +
                uuid.uuid4().hex[:8],

            "execution_id":
                execution_plan.get(
                    "id"
                ),

            "objective":
                execution_plan.get(
                    "objective"
                ),

            "agents":
                execution_plan.get(
                    "selected_agents",
                    []
                ),

            "workflow":[

                {
                    "step":
                        "Analyze objective",

                    "status":
                        "COMPLETE"
                },

                {
                    "step":
                        "Assign specialized agents",

                    "status":
                        "COMPLETE"
                },

                {
                    "step":
                        "Execute workflow",

                    "status":
                        "RUNNING"
                },

                {
                    "step":
                        "Measure outcome",

                    "status":
                        "PENDING"
                },

                {
                    "step":
                        "Store learning",

                    "status":
                        "PENDING"
                }

            ],

            "status":
                "ACTIVE",

            "started":
                time.time()

        }


        self.missions.append(
            mission
        )

        self.save()


        print(
            "🧬 Genesis Mission Started"
        )


        return mission



    def complete_step(
        self,
        mission_id,
        step_name
    ):

        for mission in self.missions:

            if mission["id"] == mission_id:

                for step in mission["workflow"]:

                    if step["step"] == step_name:

                        step["status"] = (
                            "COMPLETE"
                        )


                mission["updated"] = (
                    time.time()
                )


        self.save()


    def report(self):

        return {

            "system":
                self.system,

            "active_missions":
                len(self.missions),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_mission_execution_engine = (
    GenesisMissionExecutionEngine()
)
