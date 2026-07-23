import time
import uuid
import asyncio

from core.genesis.genesis_master_orchestrator import (
    GenesisMasterOrchestrator
)

from core.genesis.agent_registry import (
    agent_registry
)

from core.genesis.runtime.unified_agent_runtime import (
    runtime
)

from core.genesis.agent_heartbeat_system import (
    agent_heartbeat_system
)

from core.genesis.revenue.revenue_orchestrator import (
    revenue_orchestrator
)


class GenesisOperatingLoop:

    def __init__(self):

        self.system = "GENESIS AUTONOMOUS OPERATING LOOP v1"

        self.master = GenesisMasterOrchestrator()

        self.history = []


    async def execute(self, objective):

        print("""
=================================
🧬 GENESIS OPERATING LOOP ONLINE
=================================
""")

        operation = self.master.start_operation(
            objective
        )


        operation_id = operation["id"]


        agents = agent_registry.list_agents()


        if not agents:

            print(
                "⚠️ No registered agents found"
            )

            agents = [
                {
                    "name": "genesis_research_agent",
                    "skills": [
                        "research"
                    ]
                },
                {
                    "name": "genesis_revenue_agent",
                    "skills": [
                        "sales",
                        "lead_generation",
                        "revenue_strategy"
                    ]
                }
            ]


        agent_names = [
            agent["name"]
            for agent in agents
        ]


        self.master.connect_agents(
            operation_id,
            agent_names
        )


        for agent in agent_names:

            try:

                agent_heartbeat_system.heartbeat(
                    agent
                )

            except Exception:

                pass


        print(
            "🤖 Agents assigned:",
            agent_names
        )


        result = None


        if (
            "revenue" in objective.lower()
            or
            "business" in objective.lower()
            or
            "sales" in objective.lower()
            or
            "customers" in objective.lower()
        ):

            print(
                "💰 Revenue system activated"
            )


            market = objective


            result = revenue_orchestrator.run(
                market
            )


        else:

            print(
                "🧠 General agent execution activated"
            )


            result = await runtime.execute(
                agent_names[0],
                objective
            )


        mission = self.master.execute(
            operation_id
        )


        report = {

            "id":
                "genesis_cycle_" +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "operation":
                operation_id,

            "agents":
                agent_names,

            "result":
                result,

            "status":
                "COMPLETE",

            "timestamp":
                time.time()
        }


        self.history.append(
            report
        )


        print(
            """
=================================
✅ GENESIS MISSION COMPLETE
=================================
"""
        )


        return report



genesis_operating_loop = GenesisOperatingLoop()
