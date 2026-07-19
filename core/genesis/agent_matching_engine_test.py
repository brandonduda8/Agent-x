from core.genesis.agent_matching_engine import agent_matching_engine
from core.genesis.mission_intelligence_router import mission_intelligence_router


agent_matching_engine.register_agent(
    "Agent-X",
    [
        "coding",
        "flutter",
        "deployment",
        "automation"
    ]
)


agent_matching_engine.register_agent(
    "Revenue Agent",
    [
        "sales",
        "crm",
        "lead_generation",
        "outreach"
    ]
)


agent_matching_engine.register_agent(
    "Hermes",
    [
        "planning",
        "orchestration",
        "mcp"
    ]
)



mission = mission_intelligence_router.route(
    "Find and close first AI automation customer"
)



print(
    agent_matching_engine.match(
        mission
    )
)


print(
    agent_matching_engine.report()
)
