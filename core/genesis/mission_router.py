import time

from core.genesis.agent_manager import agent_manager
from core.genesis.memory_engine import memory_engine


class GenesisMissionRouter:

    def __init__(self):

        self.name = "GENESIS MISSION ROUTER v0.1"


    def analyze(self, objective):

        objective_lower = objective.lower()

        agents = []


        if any(word in objective_lower for word in [
            "research",
            "market",
            "analyze",
            "find"
        ]):
            agents.append("researcher")


        if any(word in objective_lower for word in [
            "build",
            "create",
            "code",
            "website",
            "app"
        ]):
            agents.append("builder")


        if any(word in objective_lower for word in [
            "money",
            "revenue",
            "sales",
            "business",
            "profit"
        ]):
            agents.append("revenue")


        if not agents:
            agents = list(
                agent_manager.registry.keys()
            )


        mission = {

            "id": int(time.time()),

            "objective": objective,

            "assigned_agents": agents,

            "status": "READY"

        }


        memory_engine.memory["missions"].append(
            mission
        )

        memory_engine.save()


        return mission



mission_router = GenesisMissionRouter()
