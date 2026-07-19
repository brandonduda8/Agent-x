from core.genesis.agent_evolution_engine import agent_evolution_engine


capabilities = []


result = agent_evolution_engine.evolve(
    "Revenue Agent",
    "customer_outreach_intelligence",
    capabilities
)


print(result)

print(capabilities)

print(
    agent_evolution_engine.report()
)
