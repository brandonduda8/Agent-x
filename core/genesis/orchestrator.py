import time
import asyncio
from core.genesis.agent_x_bridge import agent_x_bridge
from core.genesis.mission_router import mission_router


class GenesisOrchestrator:

    def __init__(self):
        self.name = "GENESIS MASTER ORCHESTRATOR v1"
        self.status = "ONLINE"
        self.history = []

    def boot(self):
        print("🧬 Booting Genesis Orchestrator...")
        
        connection = agent_x_bridge.connect()

        return {
            "system": self.name,
            "status": self.status,
            "agents": connection,
            "timestamp": time.time()
        }


    async def execute_mission(self, objective):

        print(
            f"""
🧬 GENESIS MISSION START

Objective:
{objective}
"""
        )

        mission = mission_router.analyze(objective)

        self.history.append(mission)

        print("📋 Mission Plan:")
        print(mission)

        return mission


    def status_report(self):

        return {
            "system": self.name,
            "status": self.status,
            "missions_completed": len(self.history),
            "timestamp": time.time()
        }



genesis_orchestrator = GenesisOrchestrator()
