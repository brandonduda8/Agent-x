import time
import uuid
import json
import os


class GenesisKnowledgeEngine:

    def __init__(self):

        self.system = "GENESIS KNOWLEDGE ENGINE v1"

        self.file = "genesis_knowledge.json"

        self.memory = {

            "knowledge": [],

            "agent_metrics": {},

            "improvements": []

        }

        self.load()



    def load(self):

        if os.path.exists(self.file):

            with open(self.file, "r") as f:

                self.memory = json.load(f)



    def save(self):

        with open(self.file, "w") as f:

            json.dump(
                self.memory,
                f,
                indent=2
            )



    def remember_build(
        self,
        project,
        lesson,
        result,
        confidence=0.8
    ):

        item = {

            "id":
            "knowledge_" + uuid.uuid4().hex[:8],

            "type":
            "BUILD_LESSON",

            "project":
            project,

            "lesson":
            lesson,

            "result":
            result,

            "confidence":
            confidence,

            "timestamp":
            time.time()

        }


        self.memory["knowledge"].append(item)

        self.save()

        return item



    def update_agent(
        self,
        agent,
        task,
        success=True
    ):

        if agent not in self.memory["agent_metrics"]:

            self.memory["agent_metrics"][agent] = {

                "tasks":0,

                "completed":0,

                "success_rate":0

            }


        data = self.memory["agent_metrics"][agent]

        data["tasks"] += 1


        if success:

            data["completed"] += 1


        data["success_rate"] = round(

            data["completed"] /
            data["tasks"],

            2

        )


        self.save()

        return data



    def create_improvement(
        self,
        area,
        change
    ):

        improvement = {

            "area":
            area,

            "change":
            change,

            "timestamp":
            time.time()

        }


        self.memory["improvements"].append(
            improvement
        )

        self.save()

        return improvement



    def report(self):

        return {

            "system":
            self.system,

            "knowledge_items":
            len(self.memory["knowledge"]),

            "agents":
            len(self.memory["agent_metrics"]),

            "improvements":
            len(self.memory["improvements"]),

            "timestamp":
            time.time()

        }



knowledge_engine = GenesisKnowledgeEngine()
