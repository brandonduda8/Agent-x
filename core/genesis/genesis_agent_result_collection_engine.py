import time
import uuid
import json
import os


class GenesisAgentResultCollectionEngine:

    def __init__(self):

        self.system = (
            "GENESIS AGENT RESULT COLLECTION ENGINE v1"
        )

        self.file = (
            "data/genesis_agent_results.json"
        )

        self.results = []

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(self.file, "r") as f:
                    data = json.load(f)
                    self.results = data.get(
                        "results",
                        []
                    )

            except:

                self.results = []


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

                    "results":
                        self.results,

                    "updated":
                        time.time()

                },
                f,
                indent=2
            )


    def collect_result(
        self,
        task,
        output
    ):

        result = {

            "id":
                "result_" +
                uuid.uuid4().hex[:8],

            "task_id":
                task.get(
                    "id"
                ),

            "mission_id":
                task.get(
                    "mission_id"
                ),

            "agent":
                task.get(
                    "agent"
                ),

            "objective":
                task.get(
                    "objective"
                ),

            "output":
                output,

            "status":
                "COMPLETE",

            "created":
                time.time()

        }


        self.results.append(
            result
        )

        self.save()


        print(
            f"🧠 Result Collected: {task.get('agent')}"
        )


        return result



    def analyze_results(self):

        successful = len(
            [
                r for r in self.results
                if r["status"] == "COMPLETE"
            ]
        )


        return {

            "system":
                self.system,

            "total_results":
                len(self.results),

            "completed":
                successful,

            "learning_signal":
                (
                    "Positive execution data"
                    if successful
                    else
                    "No execution data"
                ),

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "results":
                len(self.results),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_agent_result_collection_engine = (
    GenesisAgentResultCollectionEngine()
)
