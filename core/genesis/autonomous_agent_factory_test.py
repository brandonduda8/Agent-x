from core.genesis.autonomous_agent_factory import autonomous_agent_factory


agent = autonomous_agent_factory.spawn_from_capability_gap(
    "conversion_optimization"
)


print(agent)


print(
    autonomous_agent_factory.report()
)
