import json
import os
import time


class GenesisMemory:


    def __init__(self):

        self.path = "data/genesis_memory.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.memory = self.load()



    def load(self):

        if os.path.exists(self.path):

            try:

                with open(self.path, "r") as f:

                    data = json.load(f)


                    # Upgrade old memory formats

                    data.setdefault(
                        "agents",
                        {}
                    )

                    data.setdefault(
                        "missions",
                        []
                    )

                    data.setdefault(
                        "events",
                        []
                    )

                    data.setdefault(
                        "knowledge",
                        []
                    )

                    data.setdefault(
                        "lessons",
                        []
                    )

                    data.setdefault(
                        "performance",
                        {}
                    )


                    return data


            except Exception:

                pass


        return {

            "agents": {},

            "missions": [],

            "events": [],

            "knowledge": [],

            "lessons": [],

            "performance": {}

        }



    def save(self):

        with open(self.path, "w") as f:

            json.dump(
                self.memory,
                f,
                indent=2
            )



    def remember_agent(self, name):

        self.memory["agents"][name] = {

            "status":
                "ONLINE",

            "registered":
                time.time()

        }

        self.save()



    def remember_event(self, event):

        self.memory["events"].append({

            "time":
                time.time(),

            "event":
                event

        })

        self.save()



    def remember_knowledge(
        self,
        topic,
        information,
        confidence=0.5
    ):

        self.memory["knowledge"].append({

            "topic":
                topic,

            "information":
                information,

            "confidence":
                confidence,

            "timestamp":
                time.time()

        })

        self.save()



    def remember_lesson(
        self,
        lesson,
        source="system"
    ):

        self.memory["lessons"].append({

            "lesson":
                lesson,

            "source":
                source,

            "timestamp":
                time.time()

        })

        self.save()



    def record_performance(
        self,
        agent,
        success
    ):

        if agent not in self.memory["performance"]:

            self.memory["performance"][agent] = {

                "successes":0,

                "failures":0

            }


        if success:

            self.memory["performance"][agent]["successes"] += 1

        else:

            self.memory["performance"][agent]["failures"] += 1


        self.save()



    def recall(self, topic):

        results = []


        for item in self.memory["knowledge"]:

            if topic.lower() in item["topic"].lower():

                results.append(item)


        return results



    def report(self):

        return {

            "system":
                "GENESIS MEMORY ENGINE v2",

            "agents":
                len(self.memory["agents"]),

            "missions":
                len(self.memory["missions"]),

            "events":
                len(self.memory["events"]),

            "knowledge":
                len(self.memory["knowledge"]),

            "lessons":
                len(self.memory["lessons"]),

            "timestamp":
                time.time()

        }



memory_engine = GenesisMemory()
