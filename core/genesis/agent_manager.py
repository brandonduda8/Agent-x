import os
import json
import time


class GenesisAgentManager:


    def __init__(self):

        self.name = "GENESIS AGENT MANAGER v2"

        self.file = "data/genesis_agents.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.initialize()



    def initialize(self):

        if not os.path.exists(self.file):

            with open(
                self.file,
                "w"
            ) as f:

                json.dump(
                    {
                        "agents": {},
                        "events": []
                    },
                    f,
                    indent=2
                )



    def load(self):

        with open(
            self.file,
            "r"
        ) as f:

            return json.load(f)



    def save(
        self,
        data
    ):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )



    def register(
        self,
        name,
        capabilities=None
    ):

        data = self.load()


        agent_id = (
            name.lower()
            .replace(" ","_")
        )


        data["agents"][agent_id] = {

            "name":
                name,

            "status":
                "ONLINE",

            "capabilities":
                capabilities or [],

            "registered":
                time.time(),

            "heartbeat":
                time.time()

        }


        self.save(
            data
        )


        print(
            f"🧬 Agent registered: {name}"
        )


        return {

            "registered": True,

            "agent":
                agent_id

        }



    def heartbeat(
        self,
        agent_id
    ):

        data = self.load()


        if agent_id in data["agents"]:

            data["agents"][agent_id]["heartbeat"] = time.time()

            self.save(data)

            return True


        return False



    def update_status(
        self,
        agent_id,
        status
    ):

        data = self.load()


        if agent_id in data["agents"]:

            data["agents"][agent_id]["status"] = status

            self.save(data)


            return True


        return False



    def remove(
        self,
        agent_id
    ):

        data = self.load()


        if agent_id in data["agents"]:

            del data["agents"][agent_id]

            self.save(data)

            return True


        return False



    def list_agents(self):

        return self.load()["agents"]



    def health_report(self):

        data = self.load()

        return {

            "system":
                self.name,

            "agents":
                data,

            "timestamp":
                time.time()

        }



agent_manager = GenesisAgentManager()
