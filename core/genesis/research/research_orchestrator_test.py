from core.genesis.research.research_orchestrator import (
    research_orchestrator
)


print("="*60)
print("🌎 GENESIS AUTONOMOUS RESEARCH ENGINE TEST")
print("="*60)


result = research_orchestrator.run(
    "Healthcare AI"
)


print(result)

print(
    {
        "system":
        research_orchestrator.system
    }
)
