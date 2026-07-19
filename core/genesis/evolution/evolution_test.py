from core.genesis.evolution.agent_evolution_engine import (
    agent_evolution_engine
)


print("="*60)
print("🧬 GENESIS AGENT EVOLUTION TEST")
print("="*60)


result = agent_evolution_engine.evolve(
    "Sales Agent",
    {
        "tasks_completed":100,
        "revenue":5000,
        "customers":5
    }
)


print(result)


print(
    agent_evolution_engine.report()
)
