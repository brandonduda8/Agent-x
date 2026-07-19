import json
import os
import time
import uuid


class GenesisMissionQueue:

    def __init__(self):

        self.name = "GENESIS MISSION QUEUE v1.1"

        self.path = "data/genesis_missions.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.queue = self.load()



    def load(self):

        if os.path.exists(self.path):

            try:

                with open(self.path,"r") as f:

                    return json.load(f)

            except:

                pass


        return {
            "missions": []
        }



    def save(self):

        with open(self.path,"w") as f:

            json.dump(
                self.queue,
                f,
                indent=2
            )



    def add(self, objective, priority=5):

        mission = {

            "id":
                f"mission_{uuid.uuid4().hex[:8]}",

            "objective":
                objective,

            "priority":
                priority,

            "status":
                "QUEUED",

            "created":
                time.time()

        }


        self.queue["missions"].append(
            mission
        )

        self.save()


        print(
            f"📋 Mission queued: {objective}"
        )


        return mission



    def next(self):

        queued = [

            m for m in self.queue["missions"]

            if m["status"] == "QUEUED"

        ]


        if not queued:

            return None



        queued.sort(
            key=lambda x:x["priority"],
            reverse=True
        )


        mission = queued[0]

        mission["status"] = "ACTIVE"

        self.save()


        return mission



    def complete(self, mission_id, result):

        for mission in self.queue["missions"]:

            if mission["id"] == mission_id:

                mission["status"] = "COMPLETE"

                mission["result"] = result

                mission["completed"] = time.time()


        self.save()



    def report(self):

        return {

            "system":
                self.name,

            "missions":
                len(self.queue["missions"]),

            "queued":
                len(
                    [
                        m for m in self.queue["missions"]
                        if m["status"]=="QUEUED"
                    ]
                ),

            "timestamp":
                time.time()

        }



mission_queue = GenesisMissionQueue()
