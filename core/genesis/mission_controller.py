import time

from core.genesis.agent_registry import agent_registry
from core.genesis.conversation_memory import conversation_memory


class GenesisMissionController:

    def __init__(self):

        self.system = "GENESIS MISSION CONTROLLER v1"

        self.missions = []


    def create_mission(self, objective):

        print(
            "🎯 Genesis Mission Created:",
            objective
        )


        mission = {

            "id": f"mission_{int(time.time())}",

            "objective": objective,

            "agents": [],

            "status": "CREATED",

            "timestamp": time.time()

        }


        mission["agents"] = [

            "Digital Twin",

            "Hermes",

            "Agent-X",

            "OpenClaw"

        ]


        self.missions.append(
            mission
        )


        conversation_memory.remember(
            "Genesis",
            objective,
            "Mission created and agents assigned"
        )


        return mission



    def execute(self, objective):

        mission = self.create_mission(
            objective
        )


        mission["status"] = "EXECUTING"


        return {

            "mission": mission,

            "message":
            "Genesis agents are working on the objective."

        }



    def report(self):

        return {

            "system": self.system,

            "missions": len(self.missions),

            "timestamp": time.time()

        }



mission_controller = GenesisMissionController()
