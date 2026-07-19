import time
import uuid


class GenesisWorkforceIntelligence:

    def __init__(self):

        self.system = "GENESIS WORKFORCE INTELLIGENCE v1"
        self.agents = {}
        self.events = []


    def remember_agent(
        self,
        agent
    ):

        name = agent["name"]

        self.agents[name] = {

            "id":
                agent.get("id"),

            "name":
                name,

            "skills":
                agent.get(
                    "skills",
                    []
                ),

            "status":
                "AVAILABLE",

            "last_seen":
                time.time()
        }


        print(
            f"🧠 Workforce memory saved: {name}"
        )


        return self.agents[name]



    def find_agent(
        self,
        skill
    ):

        matches = []

        for agent in self.agents.values():

            if skill in agent["skills"]:

                matches.append(
                    agent
                )


        return matches



    def activate_existing(
        self,
        skill
    ):

        agents = self.find_agent(skill)


        if agents:

            agent = agents[0]

            agent["status"] = "ACTIVE"
            agent["last_seen"] = time.time()


            print(
                f"⚡ Existing agent activated: {agent['name']}"
            )


            return agent


        return None



    def report(self):

        return {

            "system":
                self.system,

            "agents":
                len(self.agents),

            "timestamp":
                time.time()
        }



workforce_intelligence = GenesisWorkforceIntelligence()
