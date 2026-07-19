from core.genesis.meta.genesis_brain_orchestrator import (
    genesis_brain_orchestrator
)


print("=" * 60)
print("🧠 GENESIS BRAIN ORCHESTRATOR TEST")
print("=" * 60)


result = genesis_brain_orchestrator.run(
    "Acquire first AI automation customers",
    "Healthcare AI"
)


print(result)

print(
    genesis_brain_orchestrator.report()
)
