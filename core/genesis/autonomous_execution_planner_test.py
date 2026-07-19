from core.genesis.mission_intelligence_router import mission_intelligence_router
from core.genesis.agent_matching_engine import agent_matching_engine
from core.genesis.autonomous_execution_planner import execution_planner


agent_matching_engine.register_agent(
    "Agent-X",
    [
        "coding",
        "deployment",
        "automation"
    ]
)


agent_matching_engine.register_agent(
    "Revenue Agent",
    [
        "sales",
        "crm",
        "lead_generation"
    ]
)



mission = mission_intelligence_router.route(
    "Find and close first AI automation customer"
)


match = agent_matching_engine.match(
    mission
)


plan = execution_planner.plan(
    mission,
    match["team"]
)


print(plan)

print(
    execution_planner.report()
)
