from core.genesis.global_expansion.expansion_orchestrator import (
    expansion_orchestrator
)


print("=" * 60)
print("🌎 GENESIS GLOBAL EXPANSION ENGINE TEST")
print("=" * 60)


result = expansion_orchestrator.run(
    "Expand AI automation empire"
)


print(result)

print(
    expansion_orchestrator.report()
)
