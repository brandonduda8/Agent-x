from core.genesis.evolution.agent_evolution_engine import (
    agent_evolution_engine
)

from core.genesis.evolution.evolution_bridge import (
    evolution_bridge
)


print("="*60)
print("🌉 GENESIS EVOLUTION BRIDGE TEST")
print("="*60)


evolution = agent_evolution_engine.evolve(
    "Sales Agent",
    {
        "tasks_completed":100,
        "revenue":5000,
        "customers":5
    }
)


result = evolution_bridge.deploy_evolution(
    evolution
)


print(result)


print(
    evolution_bridge.report()
)
