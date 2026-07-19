import time
import uuid

from core.genesis.worker_registry import worker_registry
from core.genesis.agent_heartbeat_system import agent_heartbeat_system
from core.genesis.agent_matching_engine import agent_matching_engine


class GenesisWorkforceActivationBridge:

    def __init__(self):

        self.system = "GENESIS WORKFORCE ACTIVATION BRIDGE v1"
        self.activations = []


    def activate_agent(self, agent):

        name = agent.get("name")
        skills = agent.get("skills", [])

        role = agent.get(
            "role",
            "Autonomous Worker"
        )


        worker = worker_registry.register_worker(
            name,
            role,
            skills
        )


        heartbeat = agent_heartbeat_system.register_agent(
            name,
            role,
            skills
        )


        matcher = agent_matching_engine.register_agent(
            name,
            skills
        )


        activation = {

            "id":
                "activation_" + uuid.uuid4().hex[:8],

            "agent":
                name,

            "worker":
                worker,

            "heartbeat":
                heartbeat,

            "matcher":
                matcher,

            "status":
                "ACTIVE",

            "timestamp":
                time.time()

        }


        self.activations.append(
            activation
        )


        print(
            f"⚡ Workforce activated: {name}"
        )


        return activation



    def activate_workforce(self, agents):

        results = []

        for agent in agents:

            results.append(
                self.activate_agent(agent)
            )


        return {

            "id":
                "activation_batch_" + uuid.uuid4().hex[:8],

            "agents":
                results,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "activations":
                len(self.activations),

            "timestamp":
                time.time()

        }



workforce_activation_bridge = GenesisWorkforceActivationBridge()
