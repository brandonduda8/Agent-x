import json
import os
import time
import uuid


class GenesisExecutiveRegistry:

    def __init__(self):

        self.system = "GENESIS EXECUTIVE REGISTRY v1"

        self.file = "data/genesis_executives.json"

        self.executives = {}

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                data = json.load(
                    open(self.file)
                )

                self.executives = data.get(
                    "executives",
                    {}
                )

            except:

                self.executives = {}


    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        json.dump(
            {
                "executives": self.executives,
                "updated": time.time()
            },
            open(self.file,"w"),
            indent=4
        )


    def appoint(
        self,
        name,
        title,
        department,
        skills
    ):

        executive = {

            "id":
                "exec_" +
                uuid.uuid4().hex[:8],

            "name":
                name,

            "title":
                title,

            "department":
                department,

            "skills":
                skills,

            "status":
                "ACTIVE",

            "appointed":
                time.time()

        }


        self.executives[name] = executive

        self.save()

        print(
            f"👑 Executive appointed: {name}"
        )

        return executive


    def get(
        self,
        name
    ):

        return self.executives.get(name)


    def list(self):

        return list(
            self.executives.values()
        )


    def report(self):

        return {

            "system":
                self.system,

            "executives":
                len(self.executives),

            "timestamp":
                time.time()

        }


executive_registry = GenesisExecutiveRegistry()
