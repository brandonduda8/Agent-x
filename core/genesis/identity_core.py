import os
import json
import time
import uuid


class GenesisIdentityCore:

    def __init__(self):

        self.system = "GENESIS IDENTITY CORE v1"

        self.file = "data/genesis_identity.json"

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
                        "identity": {
                            "name": "Genesis",
                            "version": "v1",
                            "created": time.time()
                        },

                        "agents": {},

                        "tools": {},

                        "upgrades": [],

                        "events": []

                    },

                    f,
                    indent=2

                )



    def load(self):

        with open(self.file,"r") as f:

            return json.load(f)



    def save(self,data):

        with open(self.file,"w") as f:

            json.dump(
                data,
                f,
                indent=2
            )



    def register_agent(
        self,
        name,
        role,
        skills
    ):

        data=self.load()


        if name in data["agents"]:

            return {

                "status":"EXISTS",

                "agent":
                    data["agents"][name]

            }



        agent={

            "id":
                "agent_"+uuid.uuid4().hex[:8],

            "name":
                name,

            "role":
                role,

            "skills":
                skills,

            "registered":
                time.time()

        }


        data["agents"][name]=agent


        self.save(data)


        print(
            f"🧬 Identity stored: {name}"
        )


        return agent



    def register_tool(
        self,
        name,
        category,
        purpose
    ):

        data=self.load()


        if name in data["tools"]:

            return {

                "status":"EXISTS",

                "tool":
                    data["tools"][name]

            }



        tool={

            "id":
                "tool_"+uuid.uuid4().hex[:8],

            "name":
                name,

            "category":
                category,

            "purpose":
                purpose,

            "registered":
                time.time()

        }


        data["tools"][name]=tool


        self.save(data)


        print(
            f"🔧 Identity stored tool: {name}"
        )


        return tool



    def record_upgrade(
        self,
        upgrade,
        version
    ):

        data=self.load()


        event={

            "upgrade":
                upgrade,

            "version":
                version,

            "timestamp":
                time.time()

        }


        data["upgrades"].append(event)


        self.save(data)


        return event



    def report(self):

        data=self.load()


        return {

            "system":
                self.system,

            "identity":
                data["identity"],

            "agents":
                len(data["agents"]),

            "tools":
                len(data["tools"]),

            "upgrades":
                len(data["upgrades"]),

            "timestamp":
                time.time()

        }



identity_core = GenesisIdentityCore()
