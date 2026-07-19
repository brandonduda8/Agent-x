import time
import uuid


class GenesisWorkforceActivationManager:

    def __init__(self):

        self.system = "GENESIS WORKFORCE ACTIVATION MANAGER v1"

        self.activated_agents = []

        self.events = []


    def activate_agent(
        self,
        agent,
        source="Autonomous Agent Factory"
    ):

        activated = {

            "id":
                "activation_" + uuid.uuid4().hex[:8],

            "agent":
                agent["name"],

            "skills":
                agent.get("skills", []),

            "role":
                agent.get("role"),

            "source":
                source,

            "status":
                "ACTIVE",

            "activated":
                time.time()

        }


        self.activated_agents.append(
            activated
        )


        self.events.append({

            "event":
                "AGENT_ACTIVATED",

            "agent":
                agent["name"],

            "timestamp":
                time.time()

        })


        print(
            f"⚡ Agent activated: {agent['name']}"
        )


        return activated



    def activate_workforce(
        self,
        agents
    ):

        results = []


        for agent in agents:

            results.append(
                self.activate_agent(agent)
            )


        return {

            "id":
                "workforce_activation_"
                + uuid.uuid4().hex[:8],

            "activated":
                results,

            "status":
                "READY",

            "timestamp":
                time.time()

        }



    def status(self):

        return {

            "system":
                self.system,

            "agents":
                len(self.activated_agents),

            "events":
                len(self.events),

            "timestamp":
                time.time()

        }



workforce_activation_manager = (
    GenesisWorkforceActivationManager()
)
