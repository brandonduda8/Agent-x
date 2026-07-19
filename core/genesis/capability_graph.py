import time
import uuid
import json
import os


class GenesisCapabilityGraph:

    def __init__(self):

        self.system = "GENESIS CAPABILITY GRAPH v1"

        self.file = "data/genesis_capabilities.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.initialize()



    def initialize(self):

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:

                json.dump(
                    {
                        "capabilities": {},
                        "systems": {},
                        "events": []
                    },
                    f,
                    indent=2
                )



    def load(self):

        with open(self.file, "r") as f:

            return json.load(f)



    def save(self,data):

        with open(self.file,"w") as f:

            json.dump(
                data,
                f,
                indent=2
            )



    def register_capability(
        self,
        name,
        category,
        skills,
        owner
    ):

        data=self.load()


        capability_id = (
            "cap_"
            +
            uuid.uuid4().hex[:8]
        )


        capability = {

            "id":
                capability_id,

            "name":
                name,

            "category":
                category,

            "skills":
                skills,

            "owner":
                owner,

            "status":
                "AVAILABLE",

            "created":
                time.time()

        }


        data["capabilities"][name] = capability


        self.save(data)


        print(
            f"🧬 Capability registered: {name}"
        )


        return capability



    def register_system(
        self,
        name,
        version,
        purpose
    ):

        data=self.load()


        system={

            "name":
                name,

            "version":
                version,

            "purpose":
                purpose,

            "registered":
                time.time()

        }


        data["systems"][name]=system


        self.save(data)


        print(
            f"🖥️ System registered: {name}"
        )


        return system



    def find_capabilities(
        self,
        requirement
    ):

        data=self.load()

        matches=[]


        requirement=requirement.lower()


        for name, cap in data["capabilities"].items():

            text = (
                name
                +
                " "
                +
                " ".join(cap["skills"])
            ).lower()


            if requirement in text:

                matches.append(cap)


        return matches



    def report(self):

        data=self.load()


        return {

            "system":
                self.system,

            "capabilities":
                len(data["capabilities"]),

            "systems":
                len(data["systems"]),

            "timestamp":
                time.time()

        }



capability_graph = GenesisCapabilityGraph()
