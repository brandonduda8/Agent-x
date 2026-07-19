from core.genesis.operations.agent_evolution_trigger import (
    agent_evolution_trigger
)


print("=" * 60)
print("🧬 GENESIS AGENT EVOLUTION TRIGGER TEST")
print("=" * 60)


analysis = {

    "agent":
        "Lead Generation Agent",

    "success_rate":
        0.25
}


result = agent_evolution_trigger.evaluate(
    analysis
)


print(result)

print(
    agent_evolution_trigger.report()
)
