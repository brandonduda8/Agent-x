import asyncio

from core.genesis.mission_orchestrator import GenesisMissionOrchestrator
from core.genesis.event_stream import event_stream
from core.genesis.agent_registry import agent_registry


async def main():

    agent_registry.register(
        "Revenue",
        "Sales",
        [
            "leads",
            "outreach"
        ]
    )


    orchestrator = GenesisMissionOrchestrator(
        event_stream=event_stream,
        agent_registry=agent_registry
    )


    decision = {

        "objective":
            "Find AI automation customers",

        "selected_agents":
            [
                "Revenue"
            ]
    }


    mission = orchestrator.create_mission(
        decision
    )


    print(mission)

    print(
        orchestrator.report()
    )


asyncio.run(main())
