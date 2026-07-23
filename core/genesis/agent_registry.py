import time
import uuid
import json
import os


class GenesisAgentRegistry:

    def __init__(self):

        self.system = "GENESIS PERSISTENT AGENT REGISTRY v3"

        self.file = "data/genesis_agents_registry.json"

        self.agents = {}

        self.load()


    def load(self):

        if os.path.exists(self.file):

            try:

                with open(self.file,"r") as f:

                    data=json.load(f)

                    self.agents=data.get(
                        "agents",
                        {}
                    )

            except Exception:

                self.agents={}



    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                {
                    "agents":self.agents,
                    "updated":time.time()
                },
                f,
                indent=4
            )


    def register(
        self,
        name,
        role,
        skills,
        interface="GENESIS"
    ):

        agent_id="agent_"+uuid.uuid4().hex[:8]


        agent={

            "id":agent_id,

            "name":name,

            "role":role,

            "skills":skills,

            "interface":interface,

            "status":"ONLINE",

            "available":True,

            "created":time.time()

        }


        self.agents[name]=agent


        self.save()


        print(
            f"🧬 Persistent Agent Registered: {name}"
        )


        return agent



    def get(self,name):

        return self.agents.get(name)



    def list_agents(self):

        return list(
            self.agents.values()
        )



    def find_by_skill(
        self,
        skill
    ):

        return [

            agent

            for agent in self.agents.values()

            if skill in agent["skills"]

        ]



    def report(self):

        return {

            "system":self.system,

            "agents":len(self.agents),

            "registry":self.agents,

            "timestamp":time.time()

        }



agent_registry = GenesisAgentRegistry()
