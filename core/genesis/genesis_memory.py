import time
import uuid
import json
import os


class GenesisMemory:

    def __init__(self):

        self.name = "GENESIS MEMORY SYSTEM v1"

        self.file = (
            "core/genesis/genesis_memory.json"
        )

        self.memory = {

            "missions": [],

            "lessons": [],

            "agents": {},

            "capabilities": {},

            "opportunities": {},

            "models": {}

        }

        self.load()



    def load(self):

        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    self.memory = json.load(f)

            except Exception:

                pass



    def save(self):

        os.makedirs(
            "core/genesis",
            exist_ok=True
        )

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.memory,
                f,
                indent=4
            )



    def store_mission(
        self,
        mission
    ):

        record = {

            "id":
                "memory_"
                +
                uuid.uuid4().hex[:8],

            "type":
                "mission",

            "data":
                mission,

            "timestamp":
                time.time()

        }


        self.memory["missions"].append(
            record
        )

        self.save()

        return record



    def store_lesson(
        self,
        lesson
    ):

        record = {

            "id":
                "lesson_"
                +
                uuid.uuid4().hex[:8],

            "data":
                lesson,

            "timestamp":
                time.time()

        }


        self.memory["lessons"].append(
            record
        )

        self.save()

        return record



    def update_agent_score(
        self,
        agent,
        score
    ):

        if agent not in self.memory["agents"]:

            self.memory["agents"][agent] = {

                "score": 0,

                "executions": 0

            }


        self.memory["agents"][agent]["score"] += score

        self.memory["agents"][agent]["executions"] += 1


        self.save()



    def update_capability(
        self,
        capability,
        score
    ):

        if capability not in self.memory["capabilities"]:

            self.memory["capabilities"][capability] = {

                "score": 0,

                "uses": 0

            }


        self.memory["capabilities"][capability]["score"] += score

        self.memory["capabilities"][capability]["uses"] += 1


        self.save()



    def store_opportunity(
        self,
        opportunity
    ):

        key = opportunity.get(
            "title",
            str(uuid.uuid4())
        )


        self.memory["opportunities"][key] = opportunity

        self.save()



    def store_model_result(
        self,
        model,
        score
    ):

        if model not in self.memory["models"]:

            self.memory["models"][model] = {

                "score": 0,

                "uses": 0

            }


        self.memory["models"][model]["score"] += score

        self.memory["models"][model]["uses"] += 1


        self.save()



    def recall(
        self
    ):

        return self.memory



    def report(
        self
    ):

        return {

            "system":
                self.name,

            "missions":
                len(
                    self.memory["missions"]
                ),

            "lessons":
                len(
                    self.memory["lessons"]
                ),

            "agents":
                len(
                    self.memory["agents"]
                ),

            "capabilities":
                len(
                    self.memory["capabilities"]
                ),

            "opportunities":
                len(
                    self.memory["opportunities"]
                ),

            "models":
                len(
                    self.memory["models"]
                ),

            "timestamp":
                time.time()

        }



genesis_memory = GenesisMemory()
